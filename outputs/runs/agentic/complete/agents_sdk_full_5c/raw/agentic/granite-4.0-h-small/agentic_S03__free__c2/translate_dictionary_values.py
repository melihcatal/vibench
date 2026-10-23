# translate_dictionary_values.py
from translation_client import get_translation_client
from typing import Dict, Any

def translate_dictionary_values(data: Dict[str, Any], source_lang: str = 'en', target_lang: str = 'es') -> Dict[str, Any]:
    """Translate all string values in a dictionary while preserving keys.
    Non-string values are left unchanged.
    """
    client = get_translation_client()
    translated = {}
    for key, value in data.items():
        if isinstance(value, str):
            resp = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": f"Translate the following {source_lang} text to {target_lang}:\n\n{value}"}],
                temperature=0,
            )
            translated[key] = resp.choices[0].message.content.strip()
        else:
            translated[key] = value
    return translated
