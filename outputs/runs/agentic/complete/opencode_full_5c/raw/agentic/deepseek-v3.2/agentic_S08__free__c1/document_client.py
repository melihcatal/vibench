import os
from typing import Dict, Any, Optional
from dataclasses import dataclass
import json


@dataclass
class DocumentClientConfig:
    """Configuration for document extraction clients."""

    azure_endpoint: Optional[str] = None
    azure_key: Optional[str] = None
    google_project_id: Optional[str] = None
    google_processor_id: Optional[str] = None
    google_location: Optional[str] = "us"
    openai_api_key: Optional[str] = None
    aws_access_key_id: Optional[str] = None
    aws_secret_access_key: Optional[str] = None
    aws_region: Optional[str] = "us-east-1"
    anthropic_api_key: Optional[str] = None
    pinecone_api_key: Optional[str] = None
    pinecone_environment: Optional[str] = None


class DocumentClient:
    """Client helper utilities for Structured Document Extraction."""

    def __init__(self, config: Optional[DocumentClientConfig] = None):
        self.config = config or self._load_config_from_env()
        self._clients = {}

    @staticmethod
    def _load_config_from_env() -> DocumentClientConfig:
        """Load configuration from environment variables."""
        return DocumentClientConfig(
            azure_endpoint=os.getenv("AZURE_FORM_RECOGNIZER_ENDPOINT"),
            azure_key=os.getenv("AZURE_FORM_RECOGNIZER_KEY"),
            google_project_id=os.getenv("GOOGLE_CLOUD_PROJECT_ID"),
            google_processor_id=os.getenv("GOOGLE_DOCUMENT_AI_PROCESSOR_ID"),
            google_location=os.getenv("GOOGLE_CLOUD_LOCATION", "us"),
            openai_api_key=os.getenv("OPENAI_API_KEY"),
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            aws_region=os.getenv("AWS_REGION", "us-east-1"),
            anthropic_api_key=os.getenv("ANTHROPIC_API_KEY"),
            pinecone_api_key=os.getenv("PINECONE_API_KEY"),
            pinecone_environment=os.getenv("PINECONE_ENVIRONMENT"),
        )

    def get_azure_client(self):
        """Get Azure Form Recognizer client."""
        if "azure" not in self._clients:
            from azure.ai.formrecognizer import DocumentAnalysisClient
            from azure.core.credentials import AzureKeyCredential

            if not self.config.azure_endpoint or not self.config.azure_key:
                raise ValueError("Azure endpoint and key must be configured")

            self._clients["azure"] = DocumentAnalysisClient(
                endpoint=self.config.azure_endpoint,
                credential=AzureKeyCredential(self.config.azure_key),
            )
        return self._clients["azure"]

    def get_google_client(self):
        """Get Google Document AI client."""
        if "google" not in self._clients:
            from google.cloud import documentai
            from google.api_core.client_options import ClientOptions

            if not self.config.google_project_id or not self.config.google_processor_id:
                raise ValueError(
                    "Google project ID and processor ID must be configured"
                )

            client_options = ClientOptions(
                api_endpoint=f"{self.config.google_location}-documentai.googleapis.com"
            )
            self._clients["google"] = documentai.DocumentProcessorServiceClient(
                client_options=client_options
            )
        return self._clients["google"]

    def get_openai_client(self):
        """Get OpenAI client."""
        if "openai" not in self._clients:
            from openai import OpenAI

            if not self.config.openai_api_key:
                raise ValueError("OpenAI API key must be configured")

            self._clients["openai"] = OpenAI(api_key=self.config.openai_api_key)
        return self._clients["openai"]

    def get_aws_client(self, service_name: str = "textract"):
        """Get AWS client for specified service."""
        key = f"aws_{service_name}"
        if key not in self._clients:
            import boto3

            if (
                not self.config.aws_access_key_id
                or not self.config.aws_secret_access_key
            ):
                raise ValueError("AWS credentials must be configured")

            self._clients[key] = boto3.client(
                service_name,
                aws_access_key_id=self.config.aws_access_key_id,
                aws_secret_access_key=self.config.aws_secret_access_key,
                region_name=self.config.aws_region,
            )
        return self._clients[key]

    def get_anthropic_client(self):
        """Get Anthropic client."""
        if "anthropic" not in self._clients:
            import anthropic

            if not self.config.anthropic_api_key:
                raise ValueError("Anthropic API key must be configured")

            self._clients["anthropic"] = anthropic.Anthropic(
                api_key=self.config.anthropic_api_key
            )
        return self._clients["anthropic"]

    def get_pinecone_client(self):
        """Get Pinecone client."""
        if "pinecone" not in self._clients:
            import pinecone

            if not self.config.pinecone_api_key or not self.config.pinecone_environment:
                raise ValueError("Pinecone API key and environment must be configured")

            pinecone.init(
                api_key=self.config.pinecone_api_key,
                environment=self.config.pinecone_environment,
            )
            self._clients["pinecone"] = pinecone
        return self._clients["pinecone"]

    def validate_configuration(self) -> Dict[str, bool]:
        """Validate that all required configurations are present."""
        validation = {
            "azure_configured": bool(
                self.config.azure_endpoint and self.config.azure_key
            ),
            "google_configured": bool(
                self.config.google_project_id and self.config.google_processor_id
            ),
            "openai_configured": bool(self.config.openai_api_key),
            "aws_configured": bool(
                self.config.aws_access_key_id and self.config.aws_secret_access_key
            ),
            "anthropic_configured": bool(self.config.anthropic_api_key),
            "pinecone_configured": bool(
                self.config.pinecone_api_key and self.config.pinecone_environment
            ),
        }
        return validation


# Global client instance
_client_instance: Optional[DocumentClient] = None


def get_document_client() -> DocumentClient:
    """Get or create the global document client instance."""
    global _client_instance
    if _client_instance is None:
        _client_instance = DocumentClient()
    return _client_instance


def set_document_client(client: DocumentClient) -> None:
    """Set the global document client instance (for testing)."""
    global _client_instance
    _client_instance = client
