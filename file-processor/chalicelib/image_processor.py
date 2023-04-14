
from chalice import Blueprint
import os
import requests
import uuid
import boto3

processor = Blueprint(__name__)

s3 = boto3.client('s3')
textract = boto3.client('textract',region_name='us-east-1')
sqs = boto3.client('sqs')

def process_image(image_url: str):
    text_queue_url = os.environ.get('TEXT_QUEUE_URL')
    bucket_name = os.environ.get('BUCKET_NAME')

    image_extension = image_url.split('.')[-1]
    processor.log.debug(f"Image extension: {image_extension}")

    # download image
    response = requests.get(image_url)
    if response.status_code!=200:
        processor.log.error(f'Can\'t get the file. Response status code:{response.status_code}')
        return
    
    image_data = response.content

    # save image
    object_key = f'{str(uuid.uuid4())}.{image_extension}'
    processor.log.info(f"Saving the file with name {object_key}")
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
    processor.log.info(f"Text: {text}")

    # send the text via SQS
    if text!='':
        sqs.send_message(QueueUrl=text_queue_url, MessageBody=text)
    else:
        processor.log.error("Text was not found")

    return text