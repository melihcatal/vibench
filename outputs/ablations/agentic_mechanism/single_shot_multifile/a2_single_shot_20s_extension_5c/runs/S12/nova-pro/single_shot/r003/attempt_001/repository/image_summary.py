from vision_client import VisionClient
from vision_models import VisionRequest, VisionResponse

def summarize_image(image_path):
    client = VisionClient()
    with open(image_path, 'rb') as image_file:
        image_data = image_file.read()
    label_request = VisionRequest(image_data, 'LABEL_DETECTION')
    description_request = VisionRequest(image_data, 'DOCUMENT_TEXT_DETECTION')
    labels = client.annotate(label_request.image_data, label_request.feature)
    description = client.annotate(description_request.image_data, description_request.feature)
    return {'labels': labels, 'description': description['fullTextAnnotation']['text'] if 'fullTextAnnotation' in description else ''}