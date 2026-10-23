from openai import OpenAI
from typing import Dict, Any
from security_client import get_openai_config

def check_secret_label_safety(label: str, notes: str = "") -> Dict[str, Any]:
    config = get_openai_config()
    client = OpenAI(api_key=config['api_key'])
    text = f"Label: {label}\\nNotes: {notes}"
    response = client.moderations.create(input=text)
    result = response.results[0]
    return {
        'flagged': result.flagged,
        'categories': result.categories,
        'category_scores': result.category_scores
    }
