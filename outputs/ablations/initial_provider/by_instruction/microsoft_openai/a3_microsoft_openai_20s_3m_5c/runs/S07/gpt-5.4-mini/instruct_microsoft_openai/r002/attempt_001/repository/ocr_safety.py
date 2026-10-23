from typing import Dict

from openai import OpenAI


def check_ocr_safety(text: str) -> Dict[str, str]:
    client = OpenAI()
    response = client.responses.create(
        model="gpt-5.4-mini",
        input=f"Classify whether this OCR text contains unsafe content and explain briefly: {text}",
    )
    return {"provider": "openai", "analysis": response.output_text}
