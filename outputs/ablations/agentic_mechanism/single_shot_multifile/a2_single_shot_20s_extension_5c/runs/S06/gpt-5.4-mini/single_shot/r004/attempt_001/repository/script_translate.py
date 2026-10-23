from __future__ import annotations

import os
from typing import Optional

from openai import OpenAI


def translate_script(script: str, target_language: str, source_language: Optional[str] = None) -> str:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    prompt = f"Translate the following narration script into {target_language}. Keep tone, timing, and meaning natural."
    if source_language:
        prompt += f" The source language is {source_language}."
    response = client.responses.create(model="gpt-4.1-mini", input=[{"role": "system", "content": prompt}, {"role": "user", "content": script}])
    return response.output_text
