import os
from typing import List

from openai import OpenAI


def translate_transcript(segments: List[str], target_language: str) -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    prompt = "Translate the following transcript segments into {} and preserve meaning:\n{}".format(
        target_language,
        "\n".join(segments),
    )
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You translate transcript segments accurately."},
            {"role": "user", "content": prompt},
        ],
        temperature=0,
    )
    return response.choices[0].message.content or ""
