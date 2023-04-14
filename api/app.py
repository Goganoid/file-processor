from chalice import Chalice
from chalice import BadRequestError
import os
import boto3
import logging
import re

app = Chalice(app_name='api')
sqs = boto3.client('sqs')

app.log.setLevel(logging.DEBUG)

file_url_pattern = re.compile(r"^(http(s?):)([/|.|\w|\s|-])*\.(?:jpg|png|jpeg)$")

@app.route('/', methods=['POST'])
def index():
    queue_url = os.environ.get('QUEUE_URL')
    json_data = app.current_request.json_body
    app.log.info(f"Received a json request: {json_data}")
    try:
        file_url = json_data['fileUrl']
    except KeyError:
        raise BadRequestError('Missing "fileUrl" property in JSON data')
    if file_url_pattern.match(file_url) == None:
        raise BadRequestError('"fileUrl" is not a valid link to the image file')
    sqs.send_message(QueueUrl=queue_url, MessageBody=file_url)
    app.log.info('The file URL sent to SQS successfully')
    return {'message': 'The file sent successfully','file_url':file_url}



