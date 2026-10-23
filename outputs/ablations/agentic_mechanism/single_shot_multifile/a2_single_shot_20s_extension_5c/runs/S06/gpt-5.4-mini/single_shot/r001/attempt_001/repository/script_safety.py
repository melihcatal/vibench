from __future__ import annotations

from openai import OpenAI


_SYSTEM = 'Classify narration script safety and return a concise JSON object with fields: safe, categories, rationale.'


def check_script_safety(text: str) -> dict:
    client = OpenAI()
    response = client.responses.create(
        model='gpt-4.1-mini',
        input=[
            {'role': 'system', 'content': _SYSTEM},
            {'role': 'user', 'content': text},
        ],
        temperature=0,
    )
    output = response.output_text.strip()
    return {'raw': output}
