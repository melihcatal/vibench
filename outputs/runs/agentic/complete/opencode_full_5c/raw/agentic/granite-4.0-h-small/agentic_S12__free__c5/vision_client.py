# HELPER
# Local configuration loader and client factory for vision services
import os
import json


class VisionClient:
    """Simple wrapper providing provider-specific client initialization."""

    _providers = {
        "aws": "boto3",
        "vision": "google.cloud.vision",
        # Add more as needed
    }

    def __init__(self, provider_key: str):
        # Load local config if available
        config_path = os.getenv("VISION_CONFIG_PATH", "/config/vision.json")
        self.config = json.load(open(config_path, "r"))
        self.provider = self._providers.get(provider_key)
        self._client = None

    @property
    def client(self):
        if not self._client:
            if self.provider == "boto3":
                import boto3

                self._client = boto3.client("rekognition")
            elif self.provider == "google.cloud.vision":
                from google.cloud import vision

                self._client = vision.ImageAnnotatorClient()
        return self._client

    def detect_labels(self, image_path: str):
        if self.provider == "boto3":
            with open(image_path, "rb") as f:
                response = self.client.detect_labels(Image={"Bytes": f.read()})
            return response
        elif self.provider == "google.cloud.vision":
            with open(image_path, "rb") as f:
                image = vision.Image(content=f.read())
            response = self.client.label_detection(image=image)
            return response
        raise NotImplementedError(f"Provider {self.provider} not implemented")

    def detect_text(self, image_path: str):
        if self.provider == "boto3":
            with open(image_path, "rb") as f:
                response = self.client.detect_text(Image={"Bytes": f.read()})
            return response
        elif self.provider == "google.cloud.vision":
            with open(image_path, "rb") as f:
                image = vision.Image(content=f.read())
            response = self.client.text_detection(image=image)
            return response
        raise NotImplementedError(f"Provider {self.provider} not implemented")

    def detect_objects(self, image_path: str):
        # Implement if needed
        NotImplementedError("Not required")

    def moderate_content(self, image_path: str):
        if self.provider == "boto3":
            with open(image_path, "rb") as f:
                response = self.client.DetectModerationLabels(Image={"Bytes": f.read()})
            return response
        raise NotImplementedError(f"Provider {self.provider} not implemented")

    def describe(self, image_path: str):
        if self.provider == "boto3":
            with open(image_path, "rb") as f:
                response = self.client.detect_labels(Image={"Bytes": f.read()})
            captions = [label["Name"] for label in response.get("Labels", [])]
            return {"Description": "\n".join(captions)}
        elif self.provider == "google.cloud.vision":
            with open(image_path, "rb") as f:
                image = vision.Image(content=f.read())
            response = self.client.annotate_image(
                {
                    "image": image,
                    "features": [{"type": vision.Feature.Type.OBJECT_LOCALIZATION}],
                }
            )
            # Simplified caption generation
            captions = [obj["description"] for obj in response.object_annotations]
            return {"Description": "\n".join(captions)}
        raise NotImplementedError(f"Provider {self.provider} not implemented")
