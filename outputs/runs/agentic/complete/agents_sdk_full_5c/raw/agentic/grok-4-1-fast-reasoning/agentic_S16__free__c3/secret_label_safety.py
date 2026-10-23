import os
from openai import OpenAI
from typing import Dict

def check_secret_label_safety(label: str, notes: str = '') -&gt; Dict:
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    text = f"{label} {notes}".strip()
    if not text:
        return {'flagged': False}
    response = client.moderations.create(input=text)
    result = response.results[0]
    return {
        'flagged': result.flagged,
        'categories': dict(result.categories),
        'scores': {k: float(v) for k, v in result.category_scores.items()}
    }