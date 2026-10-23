from __future__ import annotations

import json
import os
from dataclasses import asdict
from pathlib import Path
from typing import Any, Dict, Optional

from document_models import DocumentExtractionRequest, DocumentExtractionResponse, DocumentLineItem

try:
    from google.cloud import documentai  # type: ignore
except Exception:  # pragma: no cover
    documentai = None


GOOGLE_DOC_AI_ENV = "GOOGLE_APPLICATION_CREDENTIALS"


class StructuredDocumentClient:
    def __init__(self, project_id: Optional[str] = None, location: Optional[str] = None, processor_id: Optional[str] = None):
        self.project_id = project_id or os.getenv("GOOGLE_CLOUD_PROJECT")
        self.location = location or os.getenv("GOOGLE_CLOUD_LOCATION", "us")
        self.processor_id = processor_id

    def _client(self):
        if documentai is None:
            raise RuntimeError("google-cloud-documentai is required for Document AI integration")
        return documentai.DocumentProcessorServiceClient()

    def process_document(self, request: DocumentExtractionRequest) -> DocumentExtractionResponse:
        if documentai is None:
            return self._fallback_parse(request.file_path)
        client = self._client()
        processor_name = client.processor_path(self.project_id, self.location, request.processor_id or self.processor_id)
        raw_document = documentai.RawDocument(content=Path(request.file_path).read_bytes(), mime_type=request.mime_type or request.content_type)
        result = client.process_document(request={"name": processor_name, "raw_document": raw_document})
        return self._from_document_ai(result.document)

    def _from_document_ai(self, doc: Any) -> DocumentExtractionResponse:
        fields: Dict[str, Any] = {}
        for entity in getattr(doc, "entities", []) or []:
            fields[entity.type_] = entity.mention_text
        line_items = []
        for entity in getattr(doc, "entities", []) or []:
            if getattr(entity, "type_", "") == "line_item":
                line_items.append(DocumentLineItem(description=entity.mention_text, confidence=getattr(entity, "confidence", None)))
        return DocumentExtractionResponse(
            vendor=fields.get("supplier_name") or fields.get("vendor_name"),
            merchant=fields.get("merchant_name"),
            date=fields.get("invoice_date") or fields.get("transaction_date"),
            total=self._safe_float(fields.get("total_amount") or fields.get("amount_due")),
            tax=self._safe_float(fields.get("total_tax") or fields.get("tax_amount")),
            currency=fields.get("currency"),
            line_items=line_items,
            confidence=getattr(doc, "document", None) and getattr(doc.document, "mime_type", None) and 0.0,
            raw={"text": getattr(doc, "text", "")},
        )

    def _fallback_parse(self, file_path: str) -> DocumentExtractionResponse:
        text = Path(file_path).read_text(errors="ignore")
        return DocumentExtractionResponse(raw={"text": text})

    @staticmethod
    def _safe_float(value: Any) -> Optional[float]:
        try:
            if value is None:
                return None
            return float(str(value).replace(",", "").strip())
        except Exception:
            return None


def load_json_payload(payload: str) -> Dict[str, Any]:
    return json.loads(payload)


def response_to_dict(response: DocumentExtractionResponse) -> Dict[str, Any]:
    return response.to_dict()
