import os
import boto3
from google.cloud import translate_v3, documentai_v1, language_v1, aiplatform

class DocumentClient:
    """Provides client utilities and configuration for document processing services."""

    def __init__(self, config: dict = None):
        self.config = config or {}

        # AWS Textract client (for same-scenario files)
        self._textract_client = None

        # Google Cloud Translation client (for later-step files)
        self._translation_client = None
        
        # Google Cloud Vertex AI client (for later-step files)
        self._vertex_ai_client = None

        # Google Cloud Document AI client (for later-step files)
        self._document_ai_client = None

        # Google Cloud Natural Language client (for later-step files)
        self._language_client = None

    def get_textract_client(self):
        if self._textract_client is None:
            region_name = self.config.get("aws_region", os.environ.get("AWS_REGION", "us-east-1"))
            self._textract_client = boto3.client("textract", region_name=region_name)
        return self._textract_client

    def get_translation_client(self):
        if self._translation_client is None:
            self._translation_client = translate_v3.TranslationServiceClient()
        return self._translation_client

    def get_vertex_ai_client(self):
        if self._vertex_ai_client is None:
            project_id = self.config.get("gcp_project_id", os.environ.get("GCP_PROJECT_ID"))
            location = self.config.get("gcp_location", os.environ.get("GCP_LOCATION", "us-central1"))
            aiplatform.init(project=project_id, location=location)
            self._vertex_ai_client = aiplatform
        return self._vertex_ai_client

    def get_document_ai_client(self):
        if self._document_ai_client is None:
            self._document_ai_client = documentai_v1.DocumentProcessorServiceClient()
        return self._document_ai_client
    
    def get_language_client(self):
        if self._language_client is None:
            self._language_client = language_v1.LanguageServiceClient()
        return self._language_client
