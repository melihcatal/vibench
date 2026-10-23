from __future__ import annotations

from typing import Any, Dict

from openai import OpenAI

from document_models import StructuredDocumentExtractionResponse

MODEL_ID = "gpt-4o-mini"


def invoice_summary(extracted: StructuredDocumentExtractionResponse) -> Dict[str, Any]:
    client = OpenAI()
    prompt = {
        "vendor": extracted.vendor,
        "date": extracted.date,
        "total": extracted.total,
        "tax": extracted.tax,
        "line_items": extracted.line_items,
    }
    response = client.chat.completions.create(
        model=MODEL_ID,
        messages=[
            {"role": "system", "content": "Summarize invoice fields concisely."},
            {"role": "user", "content": str(prompt)},
        ],
    )
    return {"summary": response.choices[0].message.content, "model": MODEL_ID}
