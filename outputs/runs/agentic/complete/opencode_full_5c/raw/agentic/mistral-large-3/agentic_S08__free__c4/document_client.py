from typing import Dict, Any, Optional
import os
from google.cloud import documentai_v1 as documentai
from google.api_core.client_options import ClientOptions


class DocumentClient:
    def __init__(
        self, project_id: str = None, location: str = None, processor_id: str = None
    ):
        self.project_id = project_id or os.getenv("GOOGLE_CLOUD_PROJECT_ID")
        self.location = location or os.getenv("GOOGLE_CLOUD_LOCATION", "us")
        self.processor_id = processor_id or os.getenv("GOOGLE_CLOUD_PROCESSOR_ID")
        self.client = self._initialize_client()

    def _initialize_client(self) -> documentai.DocumentProcessorServiceClient:
        client_options = ClientOptions(
            api_endpoint=f"{self.location}-documentai.googleapis.com"
        )
        return documentai.DocumentProcessorServiceClient(client_options=client_options)

    def process_document(
        self, file_path: str, mime_type: str = "application/pdf"
    ) -> documentai.Document:
        with open(file_path, "rb") as file:
            content = file.read()

        name = self.client.processor_path(
            self.project_id, self.location, self.processor_id
        )
        request = documentai.ProcessRequest(
            name=name,
            raw_document=documentai.RawDocument(content=content, mime_type=mime_type),
        )
        result = self.client.process_document(request=request)
        return result.document
