from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from msrest.authentication import CognitiveServicesCredentials
from vision_models import TextDetectionResponse
from vision_client import get_azure_vision_client
import time

class AzureTextDetector:
    def __init__(self):
        self.client = get_azure_vision_client()

    def detect_text(self, image_bytes: bytes) -> TextDetectionResponse:
        poller = self.client.begin_recognize_text_in_stream(image_bytes)
        while True:
            result = poller.result()
            if poller.status() != OperationStatusCodes.running:
                break
            time.sleep(1)
        texts = []
        for region in result:
            for line in region.lines:
                texts.append(line.text)
        return TextDetectionResponse(texts=texts)

def detect_image_text(image_bytes: bytes) -> TextDetectionResponse:
    detector = AzureTextDetector()
    return detector.detect_text(image_bytes)