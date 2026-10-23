import os
from typing import Any, Dict

from openai import OpenAI

from document_client import prepare_image_input
from document_models import DocumentRequest, normalize_text_response


def extract_text(source: str, language: str = "en") -> Dict[str, Any]:
    request = DocumentRequest(source=source, language=language, features=["ocr"])
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    image_input = prepare_image_input(request)
    response = client.responses.create(
        model="gpt-5.4-mini",
        input=[
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": "Extract all readable text from this scanned document image."},
                    {"type": "input_image", "image_url": image_input["image"]},
                ],
            }
        ],
    )
    payload = {"provider": "openai", "text": response.output_text}
    return normalize_text_response(payload).__dict__
