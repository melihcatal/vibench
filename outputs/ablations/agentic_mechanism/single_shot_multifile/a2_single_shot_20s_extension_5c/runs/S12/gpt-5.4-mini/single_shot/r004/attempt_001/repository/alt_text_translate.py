import os
from typing import Dict

from openai import OpenAI

_MODEL = os.getenv("OPENAI_TRANSLATION_MODEL", "gpt-4.1-mini")


def alt_text_translate(text: str, target_language: str) -> Dict[str, str]:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    prompt = f"Translate the following image description into {target_language}. Preserve brevity and accessibility tone."
    response = client.responses.create(
        model=_MODEL,
        input=[
            {"role": "user", "content": [{"type": "input_text", "text": prompt + "\n\n" + text}]}
        ],
        temperature=0.2,
    )
    output = getattr(response, "output_text", "") or ""
    return {"translated_text": output.strip(), "raw_text": output}
