import json
import os
from typing import Any, Dict, List, Optional

from openai import OpenAI


def extract_document_fields(text: str, schema: Optional[List[str]] = None) -> Dict[str, Any]:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    fields = schema or ["document_type", "date", "total_amount", "currency", "vendor", "invoice_number"]
    prompt = (
        "Extract structured fields from OCR-normalized document text. "
        "Return only valid JSON with keys for the requested fields and values as strings or null. "
        f"Requested fields: {json.dumps(fields)}\n\n"
        f"Document text:\n{text}"
    )
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt,
        temperature=0,
    )
    output_text = getattr(response, "output_text", None)
    if not output_text:
        output_text = ""
        for item in getattr(response, "output", []) or []:
            for content in getattr(item, "content", []) or []:
                text_value = getattr(content, "text", None)
                if text_value:
                    output_text += text_value
    try:
        data = json.loads(output_text)
    except Exception:
        data = {field: None for field in fields}
        data["raw_output"] = output_text
    return data
