import os

from openai import OpenAI


def extract_document_fields(normalized_text: str):
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.responses.create(
        model=os.environ.get("OPENAI_FIELD_MODEL", "gpt-4.1-mini"),
        input=f"Extract structured fields as JSON from this OCR-normalized document text: {normalized_text}",
    )
    return response.output_text
