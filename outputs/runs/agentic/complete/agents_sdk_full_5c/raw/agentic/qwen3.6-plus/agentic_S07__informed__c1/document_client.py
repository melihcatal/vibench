"""Local configuration and client helper utilities for OCR and Layout Extraction."""

import os
from dataclasses import dataclass, field
from typing import Any

from document_models import OcrTextResponse, LayoutResponse, TableExtractionResponse, KeyValueResponse


@dataclass
class DocumentServiceConfig:
    """Centralized configuration container for document processing services."""

    aws_region: str = field(default_factory=lambda: os.environ.get("AWS_REGION", "us-east-1"))
    aws_access_key_id: str = field(default_factory=lambda: os.environ.get("AWS_ACCESS_KEY_ID", ""))
    aws_secret_access_key: str = field(default_factory=lambda: os.environ.get("AWS_SECRET_ACCESS_KEY", ""))

    azure_di_endpoint: str = field(
        default_factory=lambda: os.environ.get(
            "AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT",
            "https://<your-resource>.cognitiveservices.azure.com/",
        )
    )
    azure_di_key: str = field(default_factory=lambda: os.environ.get("AZURE_DOCUMENT_INTELLIGENCE_KEY", ""))

    google_cloud_project: str = field(default_factory=lambda: os.environ.get("GOOGLE_CLOUD_PROJECT", ""))
    google_cloud_location: str = field(default_factory=lambda: os.environ.get("GOOGLE_CLOUD_LOCATION", "us"))
    google_doc_ai_processor_id: str = field(default_factory=lambda: os.environ.get("GOOGLE_DOC_AI_PROCESSOR_ID", ""))

    mindee_api_key: str = field(default_factory=lambda: os.environ.get("MINDEE_API_KEY", ""))

    def validate_required(self, provider: str) -> None:
        """Validate that the environment variables needed for a given provider are set."""
        missing = []
        if provider == "amazon-textract":
            if not self.aws_access_key_id:
                missing.append("AWS_ACCESS_KEY_ID")
            if not self.aws_secret_access_key:
                missing.append("AWS_SECRET_ACCESS_KEY")
        elif provider == "azure-document-intelligence":
            if not self.azure_di_key or self.azure_di_endpoint.startswith("https://<your-resource>"):
                missing.extend(["AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT", "AZURE_DOCUMENT_INTELLIGENCE_KEY"])
        elif provider == "google-document-ai":
            if not self.google_cloud_project:
                missing.append("GOOGLE_CLOUD_PROJECT")
            if not self.google_doc_ai_processor_id:
                missing.append("GOOGLE_DOC_AI_PROCESSOR_ID")
        elif provider == "mindee":
            if not self.mindee_api_key:
                missing.append("MINDEE_API_KEY")

        if missing:
            raise EnvironmentError(f"Missing required environment variables for {provider}: {', '.join(missing)}")


def load_config() -> DocumentServiceConfig:
    """Load and return the service configuration from environment variables."""
    return DocumentServiceConfig()


def normalize_ocr_text_response(response: OcrTextResponse) -> dict[str, Any]:
    """Convert an OcrTextResponse into a normalized dictionary payload."""
    return {
        "full_text": response.full_text,
        "lines": [
            {"text": line["text"], "confidence": line.get("confidence"), "geometry": line.get("geometry")}
            for line in response.lines
        ],
        "words": response.words,
        "page_count": response.page_count,
        "provider": response.provider,
    }


def normalize_layout_response(response: LayoutResponse) -> dict[str, Any]:
    """Convert a LayoutResponse into a normalized dictionary payload."""
    elements = []
    for elem in response.elements:
        element_dict: dict[str, Any] = {
            "element_type": elem.element_type,
            "text": elem.text,
            "page_number": elem.page_number,
            "confidence": elem.confidence,
        }
        if elem.bounding_polygon is not None:
            element_dict["bounding_polygon"] = elem.bounding_polygon
        if elem.row_count is not None:
            element_dict["row_count"] = elem.row_count
        if elem.column_count is not None:
            element_dict["column_count"] = elem.column_count
        if elem.role is not None:
            element_dict["role"] = elem.role
        elements.append(element_dict)

    return {
        "elements": elements,
        "page_count": response.page_count,
        "provider": response.provider,
    }


def normalize_table_response(response: TableExtractionResponse) -> dict[str, Any]:
    """Convert a TableExtractionResponse into a normalized dictionary payload."""
    tables = []
    for table in response.tables:
        tables.append({
            "header_rows": [
                {
                    "row_index": row.row_index,
                    "cells": [{"text": c.text, "row_index": c.row_index, "col_index": c.col_index} for c in row.cells],
                }
                for row in table.get("header_rows", [])
            ],
            "body_rows": [
                {
                    "row_index": row.row_index,
                    "cells": [{"text": c.text, "row_index": c.row_index, "col_index": c.col_index} for c in row.cells],
                }
                for row in table.get("body_rows", [])
            ],
            "total_rows": table.get("total_rows", 0),
            "page_number": table.get("page_number"),
        })

    return {
        "tables": tables,
        "page_count": response.page_count,
        "provider": response.provider,
    }


def normalize_kv_response(response: KeyValueResponse) -> dict[str, Any]:
    """Convert a KeyValueResponse into a normalized dictionary payload."""
    return {
        "key_value_pairs": [
            {
                "key": pair.key,
                "value": pair.value,
                "confidence": pair.confidence,
                "page_number": pair.page_number,
            }
            for pair in response.key_value_pairs
        ],
        "page_count": response.page_count,
        "provider": response.provider,
    }
