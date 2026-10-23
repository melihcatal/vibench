# [LATER-STEP] appeal_translate.py
"""Translate appeal text for review using a translation provider (e.g., DeepL or libtranslate)."

from safety_client import get_openai_client

TRANSLATION_MODEL = 'gpt-4o-mini'  # provider model identifier


def translate_appeal(appeal_text: str, target_lang: str = 'en') -> str:
    """Translate appeal text into target language for reviewer consumption."""
    client = get_openai_client()
    # OpenAI's chat completion can be used for translation
    response = client.chat.completions.create(
        model=TRANSLATION_MODEL,
        messages=[{'role': 'user', 'content': f'Translate the following into {target_lang}: \n\n{appeal_text}'}],
        temperature=0.0
    )
    return response.choices[0].message.content.strip()
