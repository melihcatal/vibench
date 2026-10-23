import json
import os
import re
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from openai import OpenAI


@dataclass
class ExtractedDocumentFields:
    invoice_number: Optional[str] = None
    invoice_date: Optional[str] = None
    due_date: Optional[str] = None
    vendor_name: Optional[str] = None
    customer_name: Optional[str] = None
    total_amount: Optional[str] = None
    currency: Optional[str] = None
    line_items: Optional[List[Dict[str, Any]]] = None


class DocumentFieldExtractor:
    def __init__(self, model: str = "gpt-5.4-mini") -> None:
        self.client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        self.model = model

    def extract(self, text: str) -> Dict[str, Any]:
        normalized_text = self._normalize_text(text)
        response = self.client.responses.create(
            model=self.model,
            input=[
                {
                    "role": "system",
                    "content": (
                        "Extract structured fields from OCR-normalized document text. "
                        "Return only valid JSON with keys: invoice_number, invoice_date, due_date, "
                        "vendor_name, customer_name, total_amount, currency, line_items. "
                        "Use null when a field is missing. line_items should be a list of objects "
                        "with keys description, quantity, unit_price, amount."
                    ),
                },
                {"role": "user", "content": normalized_text},
            ],
        )
        return self._parse_json_output(response.output_text)

    def _normalize_text(self, text: str) -> str:
        text = text.strip()
        text = re.sub(r"\r\n?", "\n", text)
        text = re.sub(r"[\t ]+", " ", text)
        return text

    def _parse_json_output(self, output_text: str) -> Dict[str, Any]:
        output_text = output_text.strip()
        if output_text.startswith("```"):
            output_text = re.sub(r"^```(?:json)?\s*", "", output_text)
            output_text = re.sub(r"\s*```$", "", output_text)
        data = json.loads(output_text)
        return {
            "invoice_number": data.get("invoice_number"),
            "invoice_date": data.get("invoice_date"),
            "due_date": data.get("due_date"),
            "vendor_name": data.get("vendor_name"),
            "customer_name": data.get("customer_name"),
            "total_amount": data.get("total_amount"),
            "currency": data.get("currency"),
            "line_items": data.get("line_items") or [],
        }


def extract_document_fields(text: str) -> Dict[str, Any]:
    return DocumentFieldExtractor().extract(text)
