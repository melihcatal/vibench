from vision_client import get_rekognition_client, load_image_bytes
from vision_models import ImageTextAnnotation

def detect_image_text(image_path: str) -> ImageTextAnnotation:
    client = get_rekognition_client()
    image_bytes = load_image_bytes(image_path)
    response = client.detect_text(Image={'Bytes': image_bytes})
    detections = response['TextDetections']
    lines = [d for d in detections if d['Type'] == 'LINE']
    full_text = '\n'.join([line['DetectedText']['DetectedText'] for line in lines])
    detections_list = [
        {
            'text': d['DetectedText']['DetectedText'],
            'confidence': d['DetectedText']['Confidence'],
            'type': d['Type'],
            'id': d.get('Id')
        }
        for d in detections
    ]
    return {
        'full_text': full_text,
        'detections': detections_list
    }