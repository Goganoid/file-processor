import os
from chalice import Blueprint
from chalicelib.file_pattern import FILE_URL_PATTERN
from chalicelib.image_processor import process_file

events = Blueprint(__name__)

url_queue_name = os.environ.get('FILE_URL_QUEUE_NAME')

@events.on_sqs_message(queue=url_queue_name,batch_size=1)
def on_file_url_received(event):
    record = next(iter(event))
    events.log.info("Received a message: %s", record.body)

    image_url = record.body
    
    text=''
    if FILE_URL_PATTERN.match(image_url) == None:
        events.log.error(f'{image_url} is not a valid url to the image file')
    else:
        text = process_file(image_url)
        if text == '':
            events.log.error("Text was not found")

    return {'image_url':image_url,'text':text}
