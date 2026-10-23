import os
from typing import Optional, Dict, Any
from google.cloud import documentai_v1 as documentai
from google.api_core.client_options import ClientOptions
import backoff


class DocumentClient:
    def __init__(self):
        self.project_id = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
        self.location = os.getenv("GOOGLE_CLOUD_DOCUMENT_AI_LOCATION", "us")
        self.client_options = ClientOptions(
            api_endpoint=f"{self.location}-documentai.googleapis.com"
        )
        self.client = documentai.DocumentProcessorServiceClient(
            client_options=self.client_options
        )

    def get_processor_name(self, processor_id: str, processor_version: str) -> str:
        return self.client.processor_version_path(
            self.project_id, self.location, processor_id, processor_version
        )

    @backoff.on_exception(backoff.expo, Exception, max_tries=3)
    def process_document(
        self, processor_id: str, processor_version: str, file_path: str, mime_type: str
    ) -> documentai.Document:
        processor_name = self.get_processor_name(processor_id, processor_version)

        with open(file_path, "rb") as file:
            document_content = file.read()

        request = documentai.ProcessRequest(
            name=processor_name,
            raw_document=documentai.RawDocument(
                content=document_content, mime_type=mime_type
            ),
        )
        result = self.client.process_document(request=request)
        return result.document


def load_config() -> Dict[str, Any]:
    return {
        "invoice_processor_id": os.getenv("GOOGLE_CLOUD_INVOICE_PROCESSOR_ID"),
        "invoice_processor_version": os.getenv(
            "GOOGLE_CLOUD_INVOICE_PROCESSOR_VERSION",
            "pretrained-invoice-v1.2-2023-11-17",
        ),
        "receipt_processor_id": os.getenv("GOOGLE_CLOUD_RECEIPT_PROCESSOR_ID"),
        "receipt_processor_version": os.getenv(
            "GOOGLE_CLOUD_RECEIPT_PROCESSOR_VERSION",
            "pretrained-receipt-v1.2-2023-11-17",
        ),
    }
