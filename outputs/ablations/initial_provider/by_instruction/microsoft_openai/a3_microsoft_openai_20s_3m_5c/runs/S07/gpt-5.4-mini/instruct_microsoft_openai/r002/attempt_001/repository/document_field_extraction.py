from typing import Any, Dict

from openai import OpenAI


def extract_document_fields(text: str, schema: str = "general") -> Dict[str, Any]:
    client = OpenAI()
    response = client.responses.create(
        model="gpt-5.4-mini",
        input=f"Extract structured fields for schema {schema} from this OCR-normalized text: {text}",
    )
    return {"provider": "openai", "fields_text": response.output_text}
