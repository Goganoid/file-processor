from chalice import Chalice
from chalice import BadRequestError
import os
import logging
import boto3
import requests
import uuid
import re

file_url_pattern = re.compile(r"^(http(s?):)([/|.|\w|\s|-])*\.(?:jpg|png|jpeg)$")

app = Chalice(app_name='file-processor',debug=True)
s3 = boto3.client('s3')
textract = boto3.client('textract',region_name='us-east-1')
sqs = boto3.client('sqs')

url_queue_name = os.environ.get('IMAGE_QUEUE_NAME')

app.log.setLevel(logging.DEBUG)

def process_image(image_url):
    text_queue_url = os.environ.get('TEXT_QUEUE_URL')
    bucket_name = os.environ.get('BUCKET_NAME')

    image_extension = image_url.split('.')[-1]
    app.log.debug(f"Image extension: {image_extension}")

    # download image
    response = requests.get(image_url)
    if response.status_code!=200:
        app.log.error(f'Can\'t get the file. Response status code:{response.status_code}')
        return
    
    image_data = response.content

    # save image
    object_key = f'{str(uuid.uuid4())}.{image_extension}'
    app.log.info(f"Saving the file with name {object_key}")
    s3.put_object(Body=image_data, Bucket=bucket_name, Key=object_key)

    # extract text using Textract
    response = textract.detect_document_text(
            Document={
                'S3Object': {
                    'Bucket': bucket_name,
                    'Name': object_key
                }
            }
        )
    
    # extract the text from the Textract response
    text = ''
    for item in response['Blocks']:
        if item['BlockType'] == 'LINE':
            text += item['Text'] + ' '
    app.log.info(f"Text: {text}")

    # send the text via SQS
    if text!='':
        sqs.send_message(QueueUrl=text_queue_url, MessageBody=text)
    return text

@app.on_sqs_message(queue=url_queue_name,batch_size=1)
def on_file_url_received(event):
    record = next(iter(event))
    app.log.info("Received a message: %s", record.body)

    image_url = record.body
    
    text=''
    if file_url_pattern.match(image_url) == None:
        app.log.error(f'{image_url} is not a valid url to the image file')
    else:
        text = process_image(image_url)
        if text == '':
            app.log.error("Text was not found")

    return {'image_url':image_url,'text':text}

# this endpoint exists solely for demonstration purposes
@app.route('/', methods=['POST'])
def index():
    json_data = app.current_request.json_body
    app.log.info(f"Received json request: {json_data}")
    try:
        file_url = json_data['fileUrl']
    except KeyError:
        raise BadRequestError('Missing "fileUrl" property in JSON data')
    if file_url_pattern.match(file_url) == None:
        raise BadRequestError('"fileUrl" is not a valid link to image file')
    
    text = process_image(file_url)
    return {'image_url':file_url,'text':text}
    