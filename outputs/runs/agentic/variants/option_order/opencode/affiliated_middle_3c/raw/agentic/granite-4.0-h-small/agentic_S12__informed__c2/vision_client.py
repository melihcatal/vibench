# [HELPER] vision_client.py

import os
from google.cloud import vision as gcv  # Example; other SDKs can be swapped in via env vars


class VisionClient:
    """Local helper that abstracts the concrete provider for static image tasks.

    The concrete provider is selected via environment variables (e.g., GOOGLE_APPLICATION_CREDENTIALS, AZURE_VISION_ENDPOINT, etc.).
    """

    def __init__(self):
        # Detect which provider to instantiate based on env variables (simple heuristic)
        if os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
            self._client = gcv.ImageAnnotatorClient()
        elif os.getenv("AZURE_VISION_ENDPOINT") and os.getenv("AZURE_VISION_KEY"):
            from azure.ai.vision import VisionClient as AZClient
            credentials = AZClient.get_credentials_from_environment()
            self._client = AZClient(endpoint=os.getenv("AZURE_VISION_ENDPOINT"), credential=credentials)
        elif os.getenv("CLARIFAI_PAT"):
            from clarifai.rest import VisionAPI
            self._client = VisionAPI(os.getenv("CLARIFAI_PAT"))
        elif os.getenv("AWS_ACCESS_KEY_ID") and os.getenv("AWS_SECRET_ACCESS_KEY"):
            import boto3
            self._client = boto3.client("rekognition")
        else:
            raise RuntimeError("No supported vision provider credentials found in environment")

    def label_detection(self, image_path: str):
        """Delegate label detection to the selected provider."""
        if hasattr(self._client, "annotate_image")):  # Google style
            with gcv.Image.from_file(image_path) as img:
                response = self._client.annotate_image({"image": {"source": {"filename": image_path}}})
                return response["labelAnnotations"]
        elif hasattr(self._client, "detect_labels"):  # Azure style
            return self._client.detect_labels(image_path)
        elif hasattr(self._client, "detect_labels_v2"):  # Rekognition style
            return self._client.detect_labels(Image={'Bytes': open(image_path, 'rb').read()})
        else:  # Minimal fallback for Clarifai/etc.
            return self._client.tag(image_path)

    def describe_image(self, image_path: str):
        """Delegate image caption generation to the selected provider."""
        if hasattr(self._client, "annotate_image")):  # Google style
            with gcv.Image.from_file(image_path) as img:
                response = self._client.annotate_image({"image": {"source": {"filename": image_path}}}, features=[{"type_": "IMAGE_PROPERTIES"}])
                return response.get("textAnnotations", [])
        elif hasattr(self._client, "generate_description"):  # Azure style
            return self._client.generate_description(image_path)
        else:  # Simple generic fallback
            return self._client.label_detection(image_path)[:1]

    def text_detection(self, image_path: str):
        """Delegate OCR/text detection to the selected provider."""
        if hasattr(self._client, "annotate_image")):  # Google style
            with gcv.Image.from_file(image_path) as img:
                response = self._client.annotate_image({"image": {"source": {"filename": image_path}}}, features=[{"type_": "TEXT_DETECTION"}])
                return response.get("textAnnotations", [])
        elif hasattr(self._client, "detect_text"):  # Azure style / Rekognition
            return self._client.detect_text(image_path)
        else:
            return self._client.moderation(image_path)  # placeholder

    def moderation(self, image_path: str):
        """Delegate safety / moderation detection to the selected provider."""
        if hasattr(self._client, "annotate_image")):  # Google style
            with gcv.Image.from_file(image_path) as img:
                response = self._client.annotate_image({"image": {"source": {"filename": image_path}}}, features=[{"type_": "SAFE_SEARCH_DETECTION"}])
                return response.get("safeSearchAnnotation", [])
        elif hasattr(self._client, "detect_inappropriate_content"):  # Azure style
            return self._client.detect_inappropriate_content(image_path)
        else:
            # Generic placeholder if no concrete implementation is provided
            return []
