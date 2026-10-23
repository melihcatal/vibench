import os
from typing import Dict, Any, Optional
import json
from dataclasses import dataclass, asdict
from enum import Enum


class DocumentType(Enum):
    INVOICE = "invoice"
    RECEIPT = "receipt"
    EXPENSE_REPORT = "expense_report"
    BILL = "bill"


@dataclass
class DocumentConfig:
    """Configuration for document processing clients."""

    provider: str
    endpoint: Optional[str] = None
    api_key: Optional[str] = None
    region: Optional[str] = None
    model_id: Optional[str] = None
    timeout: int = 30

    @classmethod
    def from_env(cls, provider: str) -> "DocumentConfig":
        """Create configuration from environment variables."""
        env_prefix = provider.upper().replace("-", "_")

        return cls(
            provider=provider,
            endpoint=os.getenv(f"{env_prefix}_ENDPOINT"),
            api_key=os.getenv(f"{env_prefix}_API_KEY"),
            region=os.getenv(f"{env_prefix}_REGION"),
            model_id=os.getenv(f"{env_prefix}_MODEL_ID"),
            timeout=int(os.getenv(f"{env_prefix}_TIMEOUT", "30")),
        )


class DocumentClient:
    """Base client helper for document processing services."""

    def __init__(self, config: DocumentConfig):
        self.config = config
        self._client = None

    def get_client(self):
        """Get or create the provider-specific client."""
        if self._client is not None:
            return self._client

        if self.config.provider == "azure-form-recognizer":
            from azure.ai.formrecognizer import DocumentAnalysisClient
            from azure.core.credentials import AzureKeyCredential

            self._client = DocumentAnalysisClient(
                endpoint=self.config.endpoint,
                credential=AzureKeyCredential(self.config.api_key),
            )
        elif self.config.provider == "aws-textract":
            import boto3

            self._client = boto3.client(
                "textract",
                aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
                aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
                region_name=self.config.region or "us-east-1",
            )
        elif self.config.provider == "google-document-ai":
            from google.cloud import documentai_v1 as documentai

            self._client = documentai.DocumentProcessorServiceClient()
        elif self.config.provider == "openai":
            from openai import OpenAI

            self._client = OpenAI(api_key=self.config.api_key)
        else:
            raise ValueError(f"Unsupported provider: {self.config.provider}")

        return self._client

    def validate_config(self) -> bool:
        """Validate that required configuration is present."""
        required_fields = []

        if self.config.provider == "azure-form-recognizer":
            required_fields = ["endpoint", "api_key"]
        elif self.config.provider == "aws-textract":
            required_fields = []  # Uses AWS credentials from env
        elif self.config.provider == "google-document-ai":
            required_fields = []  # Uses Google Cloud auth
        elif self.config.provider == "openai":
            required_fields = ["api_key"]

        for field in required_fields:
            value = getattr(self.config, field, None)
            if not value:
                return False

        return True

    def get_default_model(self, document_type: DocumentType) -> str:
        """Get default model ID for document type."""
        model_map = {
            DocumentType.INVOICE: {
                "azure-form-recognizer": "prebuilt-invoice",
                "aws-textract": "ANALYZE_EXPENSE",
                "google-document-ai": "invoice_processor",
            },
            DocumentType.RECEIPT: {
                "azure-form-recognizer": "prebuilt-receipt",
                "aws-textract": "ANALYZE_EXPENSE",
                "google-document-ai": "receipt_processor",
            },
        }

        return model_map.get(document_type, {}).get(
            self.config.provider, self.config.model_id or ""
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary."""
        return asdict(self.config)
