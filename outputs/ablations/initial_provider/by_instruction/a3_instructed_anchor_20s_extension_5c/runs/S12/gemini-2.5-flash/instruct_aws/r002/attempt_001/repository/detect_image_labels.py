from vision_client import get_rekognition_client
from vision_models import DetectLabelsRequest, DetectLabelsResponse, Label

def detect_image_labels(request: DetectLabelsRequest) -> DetectLabelsResponse:
    rekognition_client = get_rekognition_client()
    response = rekognition_client.detect_labels(
        Image={'Bytes': request.image_bytes}
    )
    labels = [
        Label(name=label['Name'], confidence=label['Confidence'])
        for label in response['Labels']
    ]
    return DetectLabelsResponse(labels=labels)
