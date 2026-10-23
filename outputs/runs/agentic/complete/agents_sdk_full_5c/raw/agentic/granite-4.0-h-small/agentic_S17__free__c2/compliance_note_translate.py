import os
import requests
from typing import Dict, Any

# Simple translation service using OpenAI's ChatGPT (public API) as concrete provider
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
OPENAI_MODEL = 'gpt-4o-mini'  # concrete model identifier

def translate_compliance_note(note: str, target_lang: str = 'es') -> str:
    """Translate an English compliance note into the target language.",
    """Uses OpenAI's Chat Completions endpoint.",
    """
    if not OPENAI_API_KEY:
        raise RuntimeError('Set OPENAI_API_KEY environment variable')
    payload = {
        "model": OPENAI_MODEL,
        "messages": [{"role": "user", "content": f"Translate the following compliance note into {target_lang}:\n\n{note}"}],
        "temperature": 0.2
    }
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        json=payload,
        headers=headers,
        timeout=30
    )
    response.raise_for_status()
    result = response.json()
    # Extract translated text from model response
    translated = result["choices"][0]["message"]["content"]
    return translated.strip()

# Example usage for unit testing
if __name__ == '__main__':
    sample_note = "All data must be encrypted at rest using an approved AWS KMS key with rotation enabled."
    print(translate_compliance_note(sample_note, target_lang='fr'))
