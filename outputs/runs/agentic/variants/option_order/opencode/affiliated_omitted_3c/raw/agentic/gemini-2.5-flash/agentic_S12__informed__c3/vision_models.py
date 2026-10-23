import base64
import io


class ImageInput:
    def __init__(self, image_bytes: bytes = None, s3_object: dict = None):
        if image_bytes and s3_object:
            raise ValueError("Provide either image_bytes or s3_object, not both.")
        if not image_bytes and not s3_object:
            raise ValueError("Provide either image_bytes or s3_object.")
        self.image_bytes = image_bytes
        self.s3_object = s3_object

    def to_rekognition_input(self):
        if self.image_bytes:
            return {"Bytes": self.image_bytes}
        elif self.s3_object:
            return {"S3Object": self.s3_object}
        return {}


class RekognitionLabel:
    def __init__(self, label_data: dict):
        self.name = label_data.get("Name")
        self.confidence = label_data.get("Confidence")
        self.parents = [p.get("Name") for p in label_data.get("Parents", [])]


class RekognitionTextDetection:
    def __init__(self, text_data: dict):
        self.detected_text = text_data.get("DetectedText")
        self.type = text_data.get("Type")
        self.confidence = text_data.get("Confidence")


class RekognitionModerationLabel:
    def __init__(self, moderation_data: dict):
        self.name = moderation_data.get("Name")
        self.parent_name = moderation_data.get("ParentName")
        self.confidence = moderation_data.get("Confidence")
