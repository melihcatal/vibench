import os
from typing import List, Union

from openai import OpenAI


def translate_invoice_notes(notes: Union[str, List[str]], target_language: str = "en"):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    items = [notes] if isinstance(notes, str) else list(notes)
    prompt = (
        f"Translate the following invoice notes or descriptions into {target_language}. "
        "Preserve amounts, dates, names, and accounting terminology. Return only the translated text.\n\n"
        + "\n".join(f"- {item}" for item in items)
    )
    response = client.responses.create(
        model="gpt-5.4-mini",
        input=prompt,
    )
    return response.output_text
