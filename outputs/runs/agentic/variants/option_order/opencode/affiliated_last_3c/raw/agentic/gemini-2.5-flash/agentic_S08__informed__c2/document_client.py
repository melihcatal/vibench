import os
from typing import Tuple, Dict, Any
from google.cloud import documentai_v1beta3 as documentai
from google.api_core.client_options import ClientOptions


class DocumentAIClient:
    def __init__(
        self,
        project_id: str,
        location: str,
        processor_id: str,
        processor_version_id: str = None,
    ):
        self.project_id = project_id
        self.location = location
        self.processor_id = processor_id
        self.processor_version_id = processor_version_id

        # Setting up client options for regional endpoint
        self.client_options = ClientOptions(
            api_endpoint=f"{self.location}-documentai.googleapis.com"
        )
        self.client = documentai.DocumentProcessorServiceClient(
            client_options=self.client_options
        )

        if self.processor_version_id:
            self.processor_name = self.client.processor_version_path(
                project_id, location, processor_id, processor_version_id
            )
        else:
            self.processor_name = self.client.processor_path(
                project_id, location, processor_id
            )

    def process_document(self, content: bytes, mime_type: str) -> documentai.Document:
        raw_document = documentai.RawDocument(content=content, mime_type=mime_type)
        request = documentai.ProcessRequest(
            name=self.processor_name, raw_document=raw_document
        )
        result = self.client.process_document(request=request)
        return result.document


def get_document_ai_client(processor_type: str) -> DocumentAIClient:
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    location = os.environ.get("GOOGLE_CLOUD_LOCATION", "us")

    if processor_type == "invoice":
        processor_id = os.environ.get("GOOGLE_DOCUMENT_AI_INVOICE_PROCESSOR_ID")
        if not processor_id:
            raise ValueError(
                "GOOGLE_DOCUMENT_AI_INVOICE_PROCESSOR_ID environment variable not set"
            )
        return DocumentAIClient(project_id, location, processor_id)
    elif processor_type == "receipt":
        processor_id = os.environ.get("GOOGLE_DOCUMENT_AI_RECEIPT_PROCESSOR_ID")
        if not processor_id:
            raise ValueError(
                "GOOGLE_DOCUMENT_AI_RECEIPT_PROCESSOR_ID environment variable not set"
            )
        return DocumentAIClient(project_id, location, processor_id)
    else:
        raise ValueError(f"Unknown processor type: {processor_type}")
