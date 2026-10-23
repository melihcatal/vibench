import os
from typing import Dict, List

from openai import OpenAI

_MODEL = os.getenv("OPENAI_TEXT_MODEL", "gpt-4.1-mini")


def visual_safety_text(labels: List[str]) -> Dict[str, str]:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    prompt = "Review these visual labels for unsafe or policy-sensitive language. Return a brief assessment."
    response = client.responses.create(
        model=_MODEL,
        input=[
            {"role": "user", "content": [{"type": "input_text", "text": prompt + "\n\n" + ", ".join(labels)}]}
        ],
        temperature=0,
    )
    text = getattr(response, "output_text", "") or ""
    return {"assessment": text.strip(), "raw_text": text}
