# batch_translate.py
from translation_client import get_translation_client
from typing import List

def batch_translate(texts: List[str], source_lang: str = 'en', target_lang: str = 'es') -> List[str]:
    """Translate a list of strings while preserving order.
    Calls the provider for each string individually to keep ordering simple.
    """
    client = get_translation_client()
    translated = []
    for text in texts:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": f"Translate the following {source_lang} text to {target_lang}:\n\n{text}"}],
            temperature=0,
        )
        translated.append(response.choices[0].message.content.strip())
    return translated
