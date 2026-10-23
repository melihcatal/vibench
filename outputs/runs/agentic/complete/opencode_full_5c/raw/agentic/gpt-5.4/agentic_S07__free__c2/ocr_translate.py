from __future__ import annotations

from document_client import get_default_translation_model, get_openai_client


def translate_ocr_text(text: str, target_language: str) -> str:
    client = get_openai_client()
    response = client.responses.create(
        model=get_default_translation_model(),
        input=[
            {
                "role": "system",
                "content": [
                    {
                        "type": "input_text",
                        "text": "Translate OCR extracted document text accurately and preserve structure.",
                    }
                ],
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": f"Target language: {target_language}\n\nDocument text:\n{text}",
                    }
                ],
            },
        ],
    )
    return response.output_text
