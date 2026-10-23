import os
from typing import Literal

from google.cloud.vision_v1 import ImageAnnotatorClient
from google.cloud.vision_v1.types import AnnotateImageRequest
from google.api_core.exceptions import GoogleAPICallError

# Choose one concrete provider based on environment variable
# (Amazon Rekognition is used in the scenario files; you can switch by setting REKOGNITION_ENABLED)
USE_REKOGNITION = os.getenv('USE_REKOGNITION', 'false').lower() == 'true'


class VisionClient:
    """Thin wrapper that abstracts provider selection and common vision operations.

    The concrete service name must be supplied to the constructor and determines which
    underlying SDK client is instantiated.  Supported services:
        - 'rekognition'  -> Amazon Rekognition (default)
    
    All methods accept a dict with `{ 'Image': { 'Bytes': bytes } }` and return the raw
    provider response.
    """
    def __init__(self, service: Literal['rekognition'] = 'rekognition'):
        self.service = service
        if service == 'rekognition':
            # Amazon Rekognition SDK (boto3)
            import boto3
            self.client = boto3.client(
                'rekognition',
                # AWS credentials should be set via env vars: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
            )
        else:
            raise ValueError(f"Unsupported provider: {service}")

    def _prepare_image(self, image_path: str) -> dict:
        """Read file and prepare the payload expected by the provider."""
        with open(image_path, 'rb') as f:
            return {'Image': {'Bytes': f.read()}}

    def detect_labels(self, image_path: str) -> dict:
        """Run label/object detection (Rekognition `DetectLabels`)."""
        payload = self._prepare_image(image_path)
        if self.service == 'rekognition':
            return self.client.detect_labels(**payload)
        raise NotImplementedError

    def describe_image(self, image_path: str) -> dict:
        """Run image captioning (Rekognition `DetectText` can be repurposed for a caption-like output)."""
        payload = self._prepare_image(image_path)
        if self.service == 'rekognition':
            # Rekognition does not provide a true caption service, but we emulate a short description
            # by detecting prominent objects and returning a joined string.
            labels = self.detect_labels(image_path)['Labels']
            # Simple heuristic: join top 3 labels
            top_names = [lbl['Name'] for lbl in sorted(labels, key=lambda x: -x['Confidence'])[:3]]
            return {'Captions': [{'Caption': ' '.join(top_names)}]}
        raise NotImplementedError

    def detect_text(self, image_path: str) -> dict:
        """Run text detection (Rekognition `DetectText`)."""
        payload = self._prepare_image(image_path)
        if self.service == 'rekognition':
            return self.client.detect_text(**payload)
        raise NotImplementedError

    def detect_moderation_labels(self, image_path: str) -> dict:
        """Run unsafe content safety check (Rekognition `DetectModerationLabels`)."""
        payload = self._prepare_image(image_path)
        if self.service == 'rekognition':
            return self.client.detect_moderation_labels(**payload)
        raise NotImplementedError
