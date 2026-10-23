from typing import Dict

from openai import OpenAI


def translate_ocr_text(text: str, target_language: str = "en") -> Dict[str, str]:
    client = OpenAI()
    response = client.responses.create(
        model="gpt-5.4-mini",
        input=f"Translate this OCR text to {target_language}: {text}",
    )
    return {"provider": "openai", "translated_text": response.output_text}
