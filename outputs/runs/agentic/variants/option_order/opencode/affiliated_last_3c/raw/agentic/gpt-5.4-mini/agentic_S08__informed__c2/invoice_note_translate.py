from typing import Dict
from openai import OpenAI
from document_client import require_env


def invoice_note_translate(text: str, target_language: str = 'en') -> Dict[str, str]:
    client = OpenAI(api_key=require_env('OPENAI_API_KEY'))
    completion = client.chat.completions.create(model='gpt-4o-mini', messages=[{'role': 'user', 'content': f'Translate to {target_language}: {text}'}])
    return {'translated_text': completion.choices[0].message.content, 'provider': 'openai', 'model': 'gpt-4o-mini'}
