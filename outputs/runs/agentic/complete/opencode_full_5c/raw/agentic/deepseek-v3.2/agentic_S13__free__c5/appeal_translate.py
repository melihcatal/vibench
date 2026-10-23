import os
from typing import Dict, Any
from openai import OpenAI


def appeal_translate(appeal_text: str, target_language: str = "en") -> Dict[str, Any]:
    """
    Translate appeal text for review using OpenAI's translation capabilities.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")

    client = OpenAI(api_key=api_key)

    language_map = {
        "en": "English",
        "es": "Spanish",
        "fr": "French",
        "de": "German",
        "zh": "Chinese",
        "ja": "Japanese",
        "ko": "Korean",
        "ru": "Russian",
        "ar": "Arabic",
        "pt": "Portuguese",
    }

    target_language_name = language_map.get(target_language, "English")

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": f"You are a translation assistant. Translate text to {target_language_name} for moderation appeal review.",
            },
            {
                "role": "user",
                "content": f"Translate the following appeal text to {target_language_name}:\n\n{appeal_text}\n\nProvide both the original and translated text.",
            },
        ],
        temperature=0.1,
    )

    translated_text = response.choices[0].message.content

    return {
        "original_text": appeal_text,
        "translated_text": translated_text,
        "target_language": target_language,
        "target_language_name": target_language_name,
        "translation_provider": "OpenAI GPT-4",
    }
