import os
from typing import List

from openai import OpenAI


def batch_translate(strings: List[str], target_language: str = "Spanish") -> List[str]:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    response = client.chat.completions.create(
        model="gpt-5.4-mini",
        messages=[
            {
                "role": "system",
                "content": "Translate each input string into the target language. Preserve order and return one translation per line, with no extra text.",
            },
            {
                "role": "user",
                "content": f"Target language: {target_language}\n\nInputs:\n" + "\n".join(strings),
            },
        ],
        temperature=0,
    )
    text = response.choices[0].message.content or ""
    translations = [line.strip() for line in text.splitlines()]
    if len(translations) != len(strings):
        raise ValueError("Translation count did not match input count")
    return translations
