from __future__ import annotations

from typing import Any, Dict

from openai import OpenAI

OPENAI_MODEL = "gpt-4o-mini"


class InvoiceSummarizer:
    def __init__(self, client: OpenAI | None = None):
        self.client = client or OpenAI()

    def summarize(self, extracted_invoice: Dict[str, Any]) -> str:
        prompt = {
            "vendor": extracted_invoice.get("vendor"),
            "invoice_date": extracted_invoice.get("invoice_date"),
            "total": extracted_invoice.get("total"),
            "currency": extracted_invoice.get("currency"),
            "line_items": extracted_invoice.get("line_items", []),
        }
        response = self.client.responses.create(
            model=OPENAI_MODEL,
            input=[
                {"role": "system", "content": "Summarize invoice fields into a concise accounting review note."},
                {"role": "user", "content": str(prompt)},
            ],
        )
        return response.output_text
