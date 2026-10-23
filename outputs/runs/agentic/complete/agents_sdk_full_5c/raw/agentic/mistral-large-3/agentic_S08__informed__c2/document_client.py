import os
from typing import Optional, Dict, Any
from google.cloud import documentai_v1 as documentai
from google.api_core.client_options import ClientOptions
import boto3

class DocumentClient:
    def __init__(self):
        self.google_client = self._initialize_google_client()
        self.aws_client = self._initialize_aws_client()

    def _initialize_google_client(self) -> Optional[documentai.DocumentProcessorServiceClient]:
        if not os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
            return None
        try:
            project_id = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
            location = os.getenv("GOOGLE_DOCUMENT_AI_LOCATION", "us")
            client_options = ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com")
            return documentai.DocumentProcessorServiceClient(client_options=client_options)
        except Exception:
            return None

    def _initialize_aws_client(self):
        if not os.getenv("AWS_ACCESS_KEY_ID") or not os.getenv("AWS_SECRET_ACCESS_KEY"):
            return None
        try:
            return boto3.client(
                "textract",
                aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
                aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
                region_name=os.getenv("AWS_REGION", "us-east-1")
            )
        except Exception:
            return None

    def get_google_processor_name(self, processor_id: str) -> str:
        project_id = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
        location = os.getenv("GOOGLE_DOCUMENT_AI_LOCATION", "us")
        return f"projects/{project_id}/locations/{location}/processors/{processor_id}"

    def process_document_with_google(self, processor_id: str, file_path: str, mime_type: str = "application/pdf") -> Optional[Dict[str, Any]]:
        if not self.google_client:
            return None

        with open(file_path, "rb") as file:
            document_content = file.read()

        name = self.get_google_processor_name(processor_id)
        request = {
            "name": name,
            "raw_document": {
                "content": document_content,
                "mime_type": mime_type
            }
        }

        try:
            result = self.google_client.process_document(request=request)
            return {"document": result.document}
        except Exception:
            return None

    def process_document_with_aws(self, file_path: str) -> Optional[Dict[str, Any]]:
        if not self.aws_client:
            return None

        with open(file_path, "rb") as file:
            document_content = file.read()

        try:
            response = self.aws_client.analyze_expense(Document={'Bytes': document_content})
            return response
        except Exception:
            return None