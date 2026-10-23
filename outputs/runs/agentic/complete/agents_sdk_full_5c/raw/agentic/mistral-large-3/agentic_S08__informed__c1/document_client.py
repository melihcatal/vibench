import os
from typing import Optional
from mindee import Client as MindeeClient
from google.cloud import documentai_v1 as documentai


class DocumentClient:
    def __init__(self):
        self.mindee_client = MindeeClient(api_key=os.getenv("MINDEE_API_KEY"))
        self.google_client = documentai.DocumentProcessorServiceClient()

    def get_mindee_client(self) -> MindeeClient:
        return self.mindee_client

    def get_google_client(self) -> documentai.DocumentProcessorServiceClient:
        return self.google_client

    def get_google_processor_name(self) -> Optional[str]:
        return os.getenv("GOOGLE_DOCUMENT_AI_PROCESSOR_NAME")