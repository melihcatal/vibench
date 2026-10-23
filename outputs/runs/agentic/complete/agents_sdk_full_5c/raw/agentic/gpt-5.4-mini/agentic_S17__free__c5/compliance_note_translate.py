from __future__ import annotations

import json

from openai import OpenAI

from security_models import normalize_text



def compliance_note_translate(note: str, target_language: str = 'en') -> str:
    normalized = normalize_text(note)
    client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])
    response = client.responses.create(model='gpt-4.1-mini', input=f'Translate this compliance note into {target_language}: {normalized.text or note}')
    return json.dumps({"model": 'gpt-4.1-mini', "translation": response.output_text})
