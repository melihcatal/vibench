import os
from openai import OpenAI
from typing import Dict, Any


def appeal_translate(appeal_text: str, target_language: str = "en") -> Dict[str, Any]:
    """
    Translate appeal text for review using OpenAI's translation API.
    """
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    prompt = f"""
    Translate the following appeal text to {target_language}. 
    Preserve the tone, formality, and meaning exactly.
    
    Appeal text:
    {appeal_text}
    
    Provide only the translation.
    """

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": "You are a professional translator for moderation appeals.",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.1,
    )

    translation = response.choices[0].message.content.strip()

    return {
        "original_text": appeal_text,
        "translated_text": translation,
        "target_language": target_language,
        "translation_model": "gpt-4",
        "provider": "OpenAI",
    }
