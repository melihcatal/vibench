from typing import Any, Dict

from openai import OpenAI

from document_client import load_document_settings
from document_models import coerce_text_payload


def invoice_summary(extracted_invoice: Any) -> Dict[str, Any]:
    settings = load_document_settings()
    client = OpenAI(api_key=settings.openai_api_key)
    text = coerce_text_payload(extracted_invoice)
    response = client.responses.create(
        model=settings.openai_model,
        input=[
            {"role": "system", "content": "Summarize invoice fields concisely in JSON."},
            {"role": "user", "content": text},
        ],
        text={"format": {"type": "json_object"}},
    )
    return {"summary": getattr(response, "output_text", "")}
