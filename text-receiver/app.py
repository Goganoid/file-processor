from chalice import Chalice
import os
import logging

app = Chalice(app_name='text-receiver')

text_queue_name = os.environ.get('TEXT_QUEUE_NAME')

app.log.setLevel(logging.DEBUG)

@app.on_sqs_message(queue=text_queue_name,batch_size=1)
def on_file_url_received(event):
    app.log.info("Received message")
    record = next(iter(event))
    text = record.body
    if text == '':
        app.log.error("Text was not found")
    else: 
        app.log.info(f"Text:{text}")
