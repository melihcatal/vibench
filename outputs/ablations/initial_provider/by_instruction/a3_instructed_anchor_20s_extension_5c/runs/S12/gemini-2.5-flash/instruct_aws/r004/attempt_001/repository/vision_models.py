from typing import List, Dict, Any
from vision_client import get_rekognition_client

# Extend vision_models.py for moderation labels
class ModerationLabel:
    def __init__(self, name: str, confidence: float, parent_name: str = None):
        self.name = name
        self.confidence = confidence
        self.parent_name = parent_name

    def to_dict(self):
        return {"Name": self.name, "Confidence": self.confidence, "ParentName": self.parent_name}

class ImageSafetyResponse:
    def __init__(self, moderation_labels: List[ModerationLabel]):
        self.moderation_labels = moderation_labels

    def to_dict(self):
        return {"ModerationLabels": [label.to_dict() for label in self.moderation_labels]}
