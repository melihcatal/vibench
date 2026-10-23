import os
import json
from google.cloud import documentai_v1 as documentai
from azure.ai.documentintelligence import DocumentIntelligenceClient
from boto3 import client as boto_client


class OcrClient:
    """Unified local client that abstracts provider-specific OCR SDKs.

    Public methods:
        async_batch_annotate_files(sources) -> List[Document]  (for Google)
        begin_analyze_document(feature, image_path) -> LayoutResult (for Azure)
        start_document_text_detection(image_path) -> dict (for Amazon)
        process_document(document_data) -> Document (for Google)
    """

    def __init__(self):
        # Select provider via environment variable PROVIDER (e.g., 'google', 'azure', 'aws')
        self.provider = os.getenv("PROVIDER", "google")
        if self.provider == "google":
            self.client = documentai.DocumentProcessorServiceClient()
            self.processor = os.getenv("GOOGLE_DOCUMENTAI_PROCESSOR_ID")
        elif self.provider == "azure":
            endpoint = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT")
            key = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_KEY")
            self.client = DocumentIntelligenceClient(endpoint=endpoint, credential=key)
        elif self.provider == "aws":
            aws_key = os.getenv("AWS_ACCESS_KEY_ID")
            aws_secret = os.getenv("AWS_SECRET_ACCESS_KEY")
            self.client = boto_client(
                "textract", aws_access_key_id=aws_key, aws_secret_access_key=aws_secret
            )
        else:
            raise ValueError(f"Unsupported provider: {self.provider}")

    def async_batch_annotate_files(self, sources):
        """Google Document AI batch annotate files."""
        if self.provider != "google":
            raise NotImplementedError("Batch annotate files only supported for Google")
        return self.client.async_batch_annotate_files(
            requests=[
                documentai.types.AsyncDocumentRequest(document_source=src)
                for src in sources
            ]
        )

    def begin_analyze_document(self, feature, image_path):
        """Azure Document Intelligence analyze document."""
        if self.provider != "azure":
            raise NotImplementedError("Analyze document only supported for Azure")
        response = self.client.analyze_document(
            model_name="layout",
            feature=feature,
            document=Document.from_pdf_file(image_path),
        )
        return response

    def start_document_text_detection(self, image_path):
        """Amazon Textract start text detection job."""
        if self.provider != "aws":
            raise NotImplementedError("Start detection only supported for AWS")
        response = self.client.start_document_text_detection(
            DocumentLocation={
                "S3Object": {"Bucket": os.getenv("S3_BUCKET"), "Name": image_path}
            }
        )
        return response

    def process_document(self, document_data):
        """Google Document AI process document."""
        if self.provider != "google":
            raise NotImplementedError("Process document only supported for Google")
        response = self.client.process_document(
            parent=f"projects/{os.getenv('GOOGLE_PROJECT_ID')}/locations/{os.getenv('GOOGLE_REGION')}/processors/{self.processor}",
            document=document_data,
        )
        return response.document
