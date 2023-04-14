from chalice.test import Client
import os
# chalice `on_sqs_message` decorator requires this variable
os.environ['IMAGE_QUEUE_NAME'] = 'test'
from app import app

def test_sqs_handler_image_text():
    with Client(app) as client:
        url = 'https://previews.123rf.com/images/happyroman/happyroman1611/happyroman161100004/67968361-atm-transaction-printed-paper-receipt-bill-vector.jpg'
        response = client.lambda_.invoke(
            'on_file_url_received',
            client.events.generate_sqs_event(message_bodies=[url])
        )
        assert response.payload == {
            'image_url': url,
            'text': 'R ATM TRANSACTION TERMINAL # 65425899 SEQUNCE # 8564 DATE 15:18 08/10/2016 CARD NUMBER XXXXXXXXXXXX5698 CUSTOMER NAME JOHN EMPTY REQUSTED AMOUNT $100.00 TERMINAL FEE $1.25 TOTAL AMOUNT $101.25 '
        }

def test_sqs_handler_image_no_text():
    with Client(app) as client:
        url = 'https://upload.wikimedia.org/wikipedia/commons/thumb/b/b6/Image_created_with_a_mobile_phone.png/800px-Image_created_with_a_mobile_phone.png'
        response = client.lambda_.invoke(
            'on_file_url_received',
            client.events.generate_sqs_event(message_bodies=[url])
        )
        assert response.payload == {'image_url': url,'text': ''}

def test_sqs_handler_image_wrong_url():
    with Client(app) as client:
        url = 'https://upload.ABC.wikimedia.org/wikipedia/commons/thumb/b/b6/Image_created_with_a_mobile_phone.png/800px-Image_created_with_a_mobile_phone.png'
        response = client.lambda_.invoke(
            'on_file_url_received',
            client.events.generate_sqs_event(message_bodies=[url])
        )
        assert response.payload == {'image_url': url,'text': ''}