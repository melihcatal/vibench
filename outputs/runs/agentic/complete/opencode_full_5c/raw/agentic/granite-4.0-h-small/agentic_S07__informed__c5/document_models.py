# [HELPER] document_models.py

from __future__ import annotations
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional


# --------------------------------------------------------------------------
# Generic response envelope (used by most providers)
# --------------------------------------------------------------------------
class OcrResult(BaseModel):
    """Base model for OCR / layout / key‑value responses."""

    text: str = Field(..., description="Full extracted text (if applicable)")
    fields: Dict[str, str] = Field(
        default_factory=dict, description="Key‑value pairs when available"
    )
    tables: List[Dict[str, Any]] = Field(
        default_factory=list, description="Detected tables"
    )
    document: Dict[str, Any] = Field(
        default_factory=dict, description="Raw document JSON (provider specific)"
    )

    class Config:
        arbitrary_types_allowed = True  # allow json/dict fields


# --------------------------------------------------------------------------
# Provider‑specific models (light wrappers to keep the helper tidy)
# --------------------------------------------------------------------------


class MindeeOcrResult(BaseModel):
    """Normalized output from Mindee Document OCR."""

    text: str = Field(..., description="Plain text")
    fields: Dict[str, str] = Field(default_factory=dict, description="Key‑value pairs")
    # Mindee also returns "items", "tables", etc.; expose them under raw
    raw: Dict[str, Any] = Field(default_factory=dict, description="Raw Mindee JSON")


class AzureLayoutResult(BaseModel):
    """Normalized output from Azure Document Intelligence layout."""

    readResults: List[Dict[str, Any]] = Field(
        default_factory=list, description="Layout blocks returned by Azure"
    )


class MindeeTableResult(BaseModel):
    """Normalized table output from Mindee Invoice OCR."""

    rows: List[List[str]] = Field(default_factory=list, description="Table rows")
    columns: List[str] = Field(default_factory=list, description="Column headers")


class GoogleFormResult(BaseModel):
    """Normalized key‑value extraction from Google Document AI form parsing."""

    keyValuePairs: Dict[str, str] = Field(
        default_factory=dict, description="Key → value mapping"
    )
    raw: Dict[str, Any] = Field(
        default_factory=dict, description="Full Google Document JSON"
    )


# --------------------------------------------------------------------------
# Normalization helpers (convert any provider response into the generic envelope)
# --------------------------------------------------------------------------


def normalize_ocr_response(provider: str, raw_response: Any) -> OcrResult:
    """Map a concrete provider response to the generic OcrResult."""
    if provider == "mindee":
        return MindeeOcrResult(
            text=raw_response.get("text", ""),
            fields=raw_response.get("fields", {}),
            tables=raw_response.get("tables", []),
            raw=raw_response,
        )
    elif provider == "azure_document_intelligence":
        return AzureLayoutResult(readResults=raw_response.get("readResults", []))
    elif provider == "mindee_invoice":
        # Mindee Invoice returns rows/columns directly under each table object
        tables = []
        for tbl in raw_response.get("fields", {}).get("table", []):
            rows = [
                [cell.get("text", "") for cell in row] for row in tbl.get("rows", [])
            ]
            columns = [cell.get("text", "") for cell in tbl.get("headers", [])]
            tables.append({"rows": rows, "columns": columns})
        return OcrResult(
            text=raw_response.get("text", ""),
            fields={},
            tables=tables,
            raw=raw_response,
        )
    elif provider == "google_document_ai":
        # Simplify Google’s complex Document proto into our generic dict
        doc = raw_response.get("document", {})
        text = " ".join([t.get("text", "") for t in doc.get("tokens", [])])
        kv = {}
        for page in doc.get("pages", []):
            for kv_entry in page.get("keyValuePairs", []):
                key = kv_entry.get("key", {}).get("text", "")
                value = kv_entry.get("value", {}).get("text", "")
                kv[key] = value
        return OcrResult(text=text, fields=kv, tables=[], raw=raw_response)
    else:
        raise ValueError(f"Normalization not implemented for provider {provider}")


# --------------------------------------------------------------------------
# Example usage (local testing only)
# --------------------------------------------------------------------------
# if __name__ == "__main__":
#     from document_client import DocumentClient
#     client = DocumentClient(service="mindee_invoice")
#     raw = client.ocr("sample_invoice.jpg")
#     norm = normalize_ocr_response("mindee_invoice", raw)
#     print(norm.dict())
