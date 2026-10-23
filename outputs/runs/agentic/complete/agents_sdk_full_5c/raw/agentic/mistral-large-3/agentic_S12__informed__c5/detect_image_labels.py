import boto3
from typing import List, Dict
from vision_models import LabelDetectionResponse
from vision_client import get_aws_client

class AmazonRekognitionLabelDetector:
    def __init__(self):
        self.client = get_aws_client('rekognition')

    def detect_labels(self, image_bytes: bytes, max_labels: int = 10) -> LabelDetectionResponse:
        response = self.client.detect_labels(
            Image={'Bytes': image_bytes},
            MaxLabels=max_labels,
            MinConfidence=70
        )
        return LabelDetectionResponse(
            labels=[label['Name'] for label in response['Labels']],
            confidences=[label['Confidence'] for label in response['Labels']]
        )

def detect_image_labels(image_bytes: bytes) -> LabelDetectionResponse:
    detector = AmazonRekognitionLabelDetector()
    return detector.detect_labels(image_bytes)