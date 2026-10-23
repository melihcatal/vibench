from __future__ import annotations

import os
from typing import List

from openai import OpenAI

PROVIDER_NAME = 'OpenAI'
MODEL_ID = 'gpt-5.4-mini'


def summarize_quality_issues(text: str) -> str:
    client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])
    response = client.chat.completions.create(model=MODEL_ID, messages=[{'role': 'system', 'content': 'Summarize translation quality issues.'}, {'role': 'user', 'content': text}])
    return response.choices[0].message.content or ''
