import os
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.core.credentials import AzureKeyCredential


class AzureVisionClient:
    def __init__(self):
        self.endpoint = os.environ.get("AZURE_VISION_ENDPOINT")
        self.key = os.environ.get("AZURE_VISION_KEY")
        if not self.endpoint or not self.key:
            raise ValueError(
                "AZURE_VISION_ENDPOINT and AZURE_VISION_KEY environment variables must be set."
            )
        self.client = ImageAnalysisClient(
            endpoint=self.endpoint, credential=AzureKeyCredential(self.key)
        )

    def get_client(self) -> ImageAnalysisClient:
        return self.client
