import os
from typing import List

from openai import OpenAI

from translation_models import normalize_text


def summarize_translation_quality(issues: List[str], *, model: str = "gpt-4.1-mini") -> str:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    prompt = "\n".join(normalize_text(issue) for issue in issues)
    response = client.responses.create(
        model=model,
        input=[
            {"role": "system", "content": "You summarize translation quality issues clearly and concisely."},
            {"role": "user", "content": f"Summarize these translation quality issues:\n{prompt}"},
        ],
    )
    return getattr(response, "output_text", None) or str(response)
