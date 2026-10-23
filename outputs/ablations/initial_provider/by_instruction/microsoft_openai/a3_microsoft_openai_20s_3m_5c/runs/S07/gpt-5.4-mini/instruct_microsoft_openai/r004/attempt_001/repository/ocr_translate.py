import os

from openai import OpenAI


def translate_ocr_text(text: str, target_language: str) -> str:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.responses.create(
        model=os.environ.get("OPENAI_TRANSLATION_MODEL", "gpt-4.1-mini"),
        input=f"Translate the following OCR text into {target_language}: {text}",
    )
    return response.output_text
