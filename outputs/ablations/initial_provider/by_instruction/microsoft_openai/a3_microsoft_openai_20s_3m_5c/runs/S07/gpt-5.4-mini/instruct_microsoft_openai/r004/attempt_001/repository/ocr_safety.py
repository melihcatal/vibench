import os

from openai import OpenAI


def check_ocr_safety(text: str) -> str:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.responses.create(
        model=os.environ.get("OPENAI_SAFETY_MODEL", "gpt-4.1-mini"),
        input=f"Classify this OCR text for unsafe content and return a brief risk summary: {text}",
    )
    return response.output_text
