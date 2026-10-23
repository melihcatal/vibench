import os
from typing import Optional

from openai import OpenAI


MODEL = os.environ.get('OPENAI_TRANSLATION_MODEL', 'gpt-4o-mini')


def translate_script(script: str, target_language: str, source_language: Optional[str] = None) -> str:
    client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))
    prompt = f'Translate the following narration script into {target_language}.'
    if source_language:
        prompt += f' Source language: {source_language}.'
    resp = client.responses.create(model=MODEL, input=[{'role': 'system', 'content': 'You are a precise translation engine.'}, {'role': 'user', 'content': f'{prompt}\n\n{script}'}])
    return resp.output_text
