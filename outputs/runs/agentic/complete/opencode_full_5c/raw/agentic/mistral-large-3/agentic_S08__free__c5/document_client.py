import os
from typing import Optional, Dict, Any
from google.cloud import documentai_v1 as documentai
from google.api_core.client_options import ClientOptions
import backoff
from requests import exceptions


class DocumentClient:
    """
    Client helper for Google Cloud Document AI with retry logic and configuration.
    """

    def __init__(self):
        self.project_id = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
        self.location = os.getenv("GOOGLE_CLOUD_DOCUMENT_AI_LOCATION", "us")
        self.client_options = ClientOptions(
            api_endpoint=f"{self.location}-documentai.googleapis.com"
        )
        self.client = documentai.DocumentProcessorServiceClient(
            client_options=self.client_options
        )

    def get_processor_name(
        self, processor_id: str, processor_version: Optional[str] = None
    ) -> str:
        """
        Returns the full processor name for Google Cloud Document AI.
        """
        if processor_version:
            return self.client.processor_version_path(
                self.project_id, self.location, processor_id, processor_version
            )
        return self.client.processor_path(self.project_id, self.location, processor_id)

    @backoff.on_exception(
        backoff.expo, (exceptions.RequestException, exceptions.Timeout), max_tries=3
    )
    def process_document(
        self,
        file_path: str,
        processor_id: str,
        mime_type: str,
        processor_version: Optional[str] = None,
    ) -> documentai.Document:
        """
        Processes a document using Google Cloud Document AI with retry logic.
        """
        processor_name = self.get_processor_name(processor_id, processor_version)

        with open(file_path, "rb") as file:
            document = {"content": file.read(), "mime_type": mime_type}

        request = documentai.ProcessRequest(name=processor_name, raw_document=document)
        result = self.client.process_document(request=request)
        return result.document


def load_config() -> Dict[str, Any]:
    """
    Loads configuration for Google Cloud Document AI from environment variables.
    """
    return {
        "project_id": os.getenv("GOOGLE_CLOUD_PROJECT_ID"),
        "location": os.getenv("GOOGLE_CLOUD_DOCUMENT_AI_LOCATION", "us"),
        "invoice_processor_id": os.getenv("GOOGLE_CLOUD_INVOICE_PROCESSOR_ID"),
        "receipt_processor_id": os.getenv("GOOGLE_CLOUD_RECEIPT_PROCESSOR_ID"),
        "invoice_processor_version": os.getenv(
            "GOOGLE_CLOUD_INVOICE_PROCESSOR_VERSION",
            "pretrained-invoice-v1.0-2023-11-17",
        ),
        "receipt_processor_version": os.getenv(
            "GOOGLE_CLOUD_RECEIPT_PROCESSOR_VERSION",
            "pretrained-receipt-v1.0-2023-11-17",
        ),
    }
