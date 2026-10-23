import os
from openai import OpenAI
from model_client import OPENAI_API_KEY
from model_models import Message
from typing import List

def summarize_text(text: str) -> str:
    \"\"\"Calls OpenAI GPT-4o-mini to summarize long text.\"\"
    client = OpenAI(api_key=OPENAI_API_KEY)
    messages: List[Message] = [
        {'role': 'system', 'content': 'You are an expert at summarizing text concisely while retaining key points.'},
        {'role': 'user', 'content': f'Summarize this text:\\n\\n{text}'}
    ]
    response = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=messages,
        max_tokens=1000,
        temperature=0.3
    )
    return response.choices[0].message.content.strip()
