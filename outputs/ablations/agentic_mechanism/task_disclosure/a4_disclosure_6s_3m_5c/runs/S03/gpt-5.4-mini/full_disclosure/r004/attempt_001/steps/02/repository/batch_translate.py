import os
from typing import List, Optional

from openai import OpenAI


def batch_translate(
    texts: List[str], source_language: str, target_language: str, model: Optional[str] = None
) -> List[str]:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    chosen_model = model or "gpt-5.4-mini"
    response = client.responses.create(
        model=chosen_model,
        input=[
            {
                "role": "system",
                "content": (
                    "You are a translation engine. Translate each user-provided string from "
                    f"{source_language} to {target_language}. Preserve the input order exactly. "
                    "Return only a JSON array of translated strings, with one output per input string."
                ),
            },
            {
                "role": "user",
                "content": "\n".join(f"{index + 1}. {text}" for index, text in enumerate(texts)),
            },
        ],
    )
    translated = response.output_text.strip()
    if translated.startswith("[") and translated.endswith("]"):
        import json

        return json.loads(translated)
    raise ValueError("Model did not return a JSON array of translations")
