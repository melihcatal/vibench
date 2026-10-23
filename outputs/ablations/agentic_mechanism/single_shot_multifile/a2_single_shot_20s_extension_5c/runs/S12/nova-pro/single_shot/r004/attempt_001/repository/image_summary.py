from vision_client import get_vision_client
from vision_models import VisionRequest, VisionResponse

def image_summary(image_path):
    client = get_vision_client()
    request = VisionRequest(image_path)
    response = client.image_annotator().labelDetection(image=request.content).execute()
    vision_response = VisionResponse(response)
    labels = vision_response.get_labels()
    text = vision_response.get_text()
    safety = vision_response.get_safety()
    return {'labels': labels, 'text': text,'safety': safety}
