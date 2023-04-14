from chalice import Chalice
import logging
from chalicelib.events import events
from chalicelib.api import api
from chalicelib.image_processor import processor

app = Chalice(app_name='file-processor',debug=True)

app.log.setLevel(logging.DEBUG)

app.register_blueprint(processor)
app.register_blueprint(events)
app.register_blueprint(api)