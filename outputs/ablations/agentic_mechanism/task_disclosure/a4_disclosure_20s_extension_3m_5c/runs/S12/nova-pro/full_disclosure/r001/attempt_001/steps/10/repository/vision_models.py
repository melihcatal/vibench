from typing import Dict, Any


class VisionRequest:
    def __init__(self, image_data: bytes, model_id: str):
        self.image_data = image_data
        self.model_id = model_id

    def to_dict(self) -> Dict[str, Any]:
        return {
            'Image': {
                'Bytes': self.image_data
            },
            'ModelId': self.model_id
        }


class VisionResponse:
    def __init__(self, response_data: Dict[str, Any]):
        self.response_data = response_data

    def normalize(self) -> Dict[str, Any]:
        normalized_data = {}
        for key, value in self.response_data.items():
            normalized_data[key.lower()] = value
        return normalized_data


def normalize_labels(labels: Dict[str, Any]) -> Dict[str, Any]:
    normalized_labels = {}
    for label in labels.get('Labels', []):
        normalized_label = {
            'name': label.get('Name', ''),
            'confidence': label.get('Confidence', 0.0)
        }
        normalized_labels[normalized_label['name']] = normalized_label
    return normalized_labels