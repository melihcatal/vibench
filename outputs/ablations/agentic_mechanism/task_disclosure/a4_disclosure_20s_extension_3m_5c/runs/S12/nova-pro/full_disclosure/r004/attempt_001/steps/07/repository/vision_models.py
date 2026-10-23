from typing import Dict, Any

import boto3


class VisionModel:
    def __init__(self):
        self.client = boto3.client('rekognition')

    def detect_labels(self, image_bytes: bytes) -> Dict[str, Any]:
        response = self.client.detect_labels(
            Image={'Bytes': image_bytes},
            MaxLabels=10,
            MinConfidence=70
        )
        return response

    def detect_text(self, image_bytes: bytes) -> Dict[str, Any]:
        response = self.client.detect_text(
            Image={'Bytes': image_bytes}
        )
        return response

    def describe_image(self, image_bytes: bytes) -> Dict[str, Any]:
        response = self.client.detect_labels(
            Image={'Bytes': image_bytes},
            MaxLabels=1,
            MinConfidence=70
        )
        return response

    def normalize_response(self, response: Dict[str, Any]) -> Dict[str, Any]:
        normalized_response = {}
        for key, value in response.items():
            if isinstance(value, list):
                normalized_response[key] = [self.normalize_item(item) for item in value]
            else:
                normalized_response[key] = self.normalize_item(value)
        return normalized_response

    def normalize_item(self, item: Any) -> Any:
        if isinstance(item, dict):
            return {key: self.normalize_item(value) for key, value in item.items()}
        elif isinstance(item, list):
            return [self.normalize_item(element) for element in item]
        else:
            return item
