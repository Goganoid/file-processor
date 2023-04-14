from chalicelib.file_pattern import FILE_URL_PATTERN
from chalicelib.image_processor import process_image
from chalice import BadRequestError
from chalice import Blueprint

api = Blueprint(__name__)

# this endpoint exists solely for demonstration purposes
@api.route('/', methods=['POST'])
def index():
    json_data = api.current_request.json_body
    api.log.info(f"Received json request: {json_data}")
    try:
        file_url = json_data['fileUrl']
    except KeyError:
        raise BadRequestError('Missing "fileUrl" property in JSON data')
    if FILE_URL_PATTERN.match(file_url) == None:
        raise BadRequestError('"fileUrl" is not a valid link to image file')
    
    text = process_image(file_url)
    return {'image_url':file_url,'text':text}