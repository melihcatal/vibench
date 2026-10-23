import os
import json
from typing import Dict, Any, Optional
from dataclasses import dataclass
from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient


@dataclass
class DocumentClientConfig:
    """Configuration for document processing clients."""

    azure_endpoint: str = os.getenv(
        "AZURE_FORM_RECOGNIZER_ENDPOINT",
        "https://your-endpoint.cognitiveservices.azure.com/",
    )
    azure_key: str = os.getenv("AZURE_FORM_RECOGNIZER_KEY", "")
    google_project_id: str = os.getenv("GOOGLE_CLOUD_PROJECT", "")
    google_processor_id: str = os.getenv("DOCUMENT_AI_PROCESSOR_ID", "")
    aws_region: str = os.getenv("AWS_REGION", "us-east-1")
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    default_model: str = "prebuilt-invoice"


class DocumentClient:
    """Client helper for document processing services."""

    def __init__(self, config: Optional[DocumentClientConfig] = None):
        self.config = config or DocumentClientConfig()
        self._azure_client = None
        self._google_client = None
        self._aws_client = None
        self._openai_client = None

    @property
    def azure_client(self) -> DocumentAnalysisClient:
        """Lazy initialization of Azure Form Recognizer client."""
        if self._azure_client is None:
            credential = AzureKeyCredential(self.config.azure_key)
            self._azure_client = DocumentAnalysisClient(
                endpoint=self.config.azure_endpoint, credential=credential
            )
        return self._azure_client

    def get_google_client(self):
        """Get Google Document AI client."""
        if self._google_client is None:
            from google.cloud import documentai

            self._google_client = documentai.DocumentProcessorServiceClient()
        return self._google_client

    def get_aws_client(self, service_name: str = "textract"):
        """Get AWS client for specified service."""
        import boto3

        if service_name == "textract":
            if self._aws_client is None:
                self._aws_client = boto3.client(
                    "textract",
                    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
                    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
                    region_name=self.config.aws_region,
                )
            return self._aws_client
        return None

    def get_openai_client(self):
        """Get OpenAI client."""
        if self._openai_client is None:
            import openai

            openai.api_key = self.config.openai_api_key
            self._openai_client = openai
        return self._openai_client

    def validate_configuration(self) -> Dict[str, bool]:
        """Validate that required environment variables are set."""
        validation = {
            "azure_configured": bool(
                self.config.azure_key and self.config.azure_endpoint
            ),
            "google_configured": bool(
                self.config.google_project_id and self.config.google_processor_id
            ),
            "aws_configured": bool(
                os.getenv("AWS_ACCESS_KEY_ID") and os.getenv("AWS_SECRET_ACCESS_KEY")
            ),
            "openai_configured": bool(self.config.openai_api_key),
        }
        return validation

    def get_supported_models(self) -> Dict[str, List[str]]:
        """Get list of supported models by service."""
        return {
            "azure": [
                "prebuilt-invoice",
                "prebuilt-receipt",
                "prebuilt-layout",
                "prebuilt-document",
            ],
            "google": ["receipt", "invoice", "form"],
            "aws": ["textract"],
        }


# Global client instance
_client_instance = None


def get_document_client(
    config: Optional[DocumentClientConfig] = None,
) -> DocumentClient:
    """Get or create a global document client instance."""
    global _client_instance
    if _client_instance is None:
        _client_instance = DocumentClient(config)
    return _client_instance


def load_config_from_file(file_path: str) -> DocumentClientConfig:
    """Load configuration from a JSON file."""
    with open(file_path, "r") as f:
        config_data = json.load(f)

    return DocumentClientConfig(
        azure_endpoint=config_data.get("azure_endpoint", ""),
        azure_key=config_data.get("azure_key", ""),
        google_project_id=config_data.get("google_project_id", ""),
        google_processor_id=config_data.get("google_processor_id", ""),
        aws_region=config_data.get("aws_region", "us-east-1"),
        openai_api_key=config_data.get("openai_api_key", ""),
    )
