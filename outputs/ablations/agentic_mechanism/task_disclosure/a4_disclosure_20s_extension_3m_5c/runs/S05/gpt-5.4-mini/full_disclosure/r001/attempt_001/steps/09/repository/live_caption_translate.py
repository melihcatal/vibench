import os
from typing import List

from openai import OpenAI


def translate_live_captions(captions: List[str], target_language: str) -> List[str]:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    translated: List[str] = []
    for caption in captions:
        resp = client.responses.create(
            model="gpt-4.1-mini",
            input=[
                {
                    "role": "system",
                    "content": f"Translate live captions into {target_language}. Return only the translation.",
                },
                {"role": "user", "content": caption},
            ],
        )
        translated.append(resp.output_text)
    return translated
