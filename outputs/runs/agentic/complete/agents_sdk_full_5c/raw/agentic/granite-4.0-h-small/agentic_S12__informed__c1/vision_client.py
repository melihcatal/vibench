import os
from aliyun.openapi.vision import VisionApi

class VisionClient:
    """Provide a thin wrapper around the Alibaba Cloud Vision API SDK."""
    def __init__(self):
        # Environment variable ALIBABA_CLOUD_ACCESS_KEY_ID / ALIBABA_CLOUD_ACCESS_KEY_SECRET are required
        self.vision_api = VisionApi()
        # Auto-load credentials from env; SDK will raise if missing
    
    def detect_objects(self, image: bytes) -> dict:
        """Call the object detection endpoint."""
        return self.vision_api.detectObjects(image=image)

    def describe_image(self, image: bytes) -> dict:
        """Call the image description endpoint."""
        return self.vision_api.describeImage(image=image)

    def detect_text(self, image: bytes) -> dict:
        """Call the text detection endpoint."""
        return self.vision_api.detectText(image=image)

    def detect_safety(self, image: bytes) -> dict:
        """Call the safety detection endpoint."""
        return self.vision_api.detectSafety(image=image)
