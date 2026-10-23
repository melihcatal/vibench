from vision_client import get_rekognition_client
from vision_models import VisionResponse

def summarize_image_analysis(image_path):
    client = get_rekognition_client()
    labels = client.detect_labels(Image={'Bytes': open(image_path, 'rb').read()})['Labels']
    text = client.detect_text(Image={'Bytes': open(image_path, 'rb').read()})['TextDetections']
    safety = client.detect_moderation_labels(Image={'Bytes': open(image_path, 'rb').read()})['ModerationLabels']
    return VisionResponse(labels=labels, text=text, safety=safety)