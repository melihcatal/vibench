import os
import json
from typing import Dict, Any, Optional
from enum import Enum


class DocumentType(Enum):
    INVOICE = "invoice"
    RECEIPT = "receipt"
    EXPENSE = "expense"


class DocumentClient:
    def __init__(self):
        self.config = self._load_config()
        self.clients = self._initialize_clients()

    def _load_config(self) -> Dict[str, Any]:
        config = {
            "azure_document_intelligence": {
                "endpoint": os.getenv("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT"),
                "key": os.getenv("AZURE_DOCUMENT_INTELLIGENCE_KEY"),
                "enabled": bool(os.getenv("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT")),
            },
            "mindee": {
                "api_key": os.getenv("MINDEE_API_KEY"),
                "enabled": bool(os.getenv("MINDEE_API_KEY")),
            },
            "google_document_ai": {
                "project_id": os.getenv("GOOGLE_DOCUMENT_AI_PROJECT_ID"),
                "location": os.getenv("GOOGLE_DOCUMENT_AI_LOCATION", "us"),
                "processor_id": os.getenv("GOOGLE_DOCUMENT_AI_PROCESSOR_ID"),
                "enabled": bool(os.getenv("GOOGLE_DOCUMENT_AI_PROJECT_ID")),
            },
        }
        return config

    def _initialize_clients(self) -> Dict[str, Any]:
        clients = {}

        if self.config["azure_document_intelligence"]["enabled"]:
            try:
                from azure.ai.documentintelligence import DocumentIntelligenceClient
                from azure.core.credentials import AzureKeyCredential

                clients["azure"] = DocumentIntelligenceClient(
                    endpoint=self.config["azure_document_intelligence"]["endpoint"],
                    credential=AzureKeyCredential(
                        self.config["azure_document_intelligence"]["key"]
                    ),
                )
            except ImportError:
                pass

        if self.config["mindee"]["enabled"]:
            try:
                from mindee import Client

                clients["mindee"] = Client(api_key=self.config["mindee"]["api_key"])
            except ImportError:
                pass

        return clients

    def get_client(self, provider: str) -> Optional[Any]:
        return self.clients.get(provider)

    def is_provider_available(self, provider: str) -> bool:
        return provider in self.clients

    def get_available_providers(self) -> list:
        return list(self.clients.keys())

    def get_provider_for_document_type(self, doc_type: DocumentType) -> str:
        provider_preferences = {
            DocumentType.INVOICE: ["azure", "mindee"],
            DocumentType.RECEIPT: ["mindee", "azure"],
            DocumentType.EXPENSE: ["azure", "mindee"],
        }

        for provider in provider_preferences.get(doc_type, []):
            if self.is_provider_available(provider):
                return provider

        available = self.get_available_providers()
        return available[0] if available else None

    def create_extraction_request(
        self, image_path: str, doc_type: DocumentType
    ) -> Dict[str, Any]:
        provider = self.get_provider_for_document_type(doc_type)

        if not provider:
            raise ValueError("No document extraction provider available")

        with open(image_path, "rb") as f:
            file_content = f.read()

        request = {
            "provider": provider,
            "document_type": doc_type.value,
            "content": file_content,
            "content_type": "application/octet-stream",
            "timestamp": os.path.getmtime(image_path),
        }

        return request

    def parse_extraction_response(
        self, response: Any, provider: str, doc_type: DocumentType
    ) -> Dict[str, Any]:
        if provider == "azure":
            return self._parse_azure_response(response, doc_type)
        elif provider == "mindee":
            return self._parse_mindee_response(response, doc_type)
        else:
            raise ValueError(f"Unsupported provider: {provider}")

    def _parse_azure_response(
        self, response: Any, doc_type: DocumentType
    ) -> Dict[str, Any]:
        parsed = {
            "provider": "azure",
            "document_type": doc_type.value,
            "fields": {},
            "confidence": response.documents[0].confidence
            if hasattr(response.documents[0], "confidence")
            else None,
        }

        for field_name, field in response.documents[0].fields.items():
            field_value = None
            if hasattr(field, "value_string") and field.value_string:
                field_value = field.value_string
            elif hasattr(field, "value_number") and field.value_number:
                field_value = field.value_number
            elif hasattr(field, "value_date") and field.value_date:
                field_value = field.value_date

            parsed["fields"][field_name] = {
                "value": field_value,
                "confidence": field.confidence
                if hasattr(field, "confidence")
                else None,
            }

        return parsed

    def _parse_mindee_response(
        self, response: Any, doc_type: DocumentType
    ) -> Dict[str, Any]:
        parsed = {
            "provider": "mindee",
            "document_type": doc_type.value,
            "fields": {},
            "confidence": response.document.inference.confidence
            if hasattr(response.document.inference, "confidence")
            else None,
        }

        document = response.document

        for attr_name in dir(document):
            if not attr_name.startswith("_"):
                attr = getattr(document, attr_name)
                if hasattr(attr, "value"):
                    parsed["fields"][attr_name] = {
                        "value": attr.value,
                        "confidence": attr.confidence
                        if hasattr(attr, "confidence")
                        else None,
                    }

        return parsed
