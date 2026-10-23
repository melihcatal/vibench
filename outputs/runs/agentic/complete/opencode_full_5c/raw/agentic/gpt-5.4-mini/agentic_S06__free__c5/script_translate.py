import os
from typing import Optional

from openai import OpenAI


def script_translate(text: str, target_language: str, source_language: Optional[str] = None) -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    prompt = f"Translate the following narration script into {target_language}."
    if source_language:
        prompt += f" Source language: {source_language}."
    response = client.responses.create(model="gpt-4.1-mini", input=[{"role": "system", "content": prompt}, {"role": "user", "content": text}])
    return response.output_text
