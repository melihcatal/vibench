import os
from typing import Dict, Any
import openai


def appeal_translate(appeal_text: str, target_language: str = "en") -> Dict[str, Any]:
    """
    Translate appeal text for review using OpenAI's translation capabilities.
    """
    client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

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
                "content": f"You are a professional translator specializing in content moderation appeals. Translate the text accurately while preserving tone and intent.",
            },
            {
                "role": "user",
                "content": f"Translate this content moderation appeal to {target_language_name}. Preserve the original meaning and tone:\n\n{appeal_text}",
            },
        ],
        temperature=0.2,
        max_tokens=500,
    )

    translated_text = response.choices[0].message.content.strip()

    return {
        "original_text": appeal_text,
        "translated_text": translated_text,
        "target_language": target_language,
        "target_language_name": target_language_name,
        "translation_provider": "OpenAI GPT-4",
        "character_count": len(appeal_text),
        "translated_character_count": len(translated_text),
    }


def translate_with_context(
    appeal_text: str, moderation_context: Dict[str, Any], target_language: str = "en"
) -> Dict[str, Any]:
    """
    Translate appeal text with moderation context for better accuracy.
    """
    client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    context_summary = f"""
    Moderation Context:
    - Flagged: {moderation_context.get("flagged", False)}
    - Categories: {moderation_context.get("categories", {})}
    - Original decision: {moderation_context.get("decision", "unknown")}
    """

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": "You are a translator for content moderation appeals. Consider the moderation context to ensure accurate translation of technical terms and appeals language.",
            },
            {
                "role": "user",
                "content": f"Context: {context_summary}\n\nTranslate this appeal text to {target_language}:\n\n{appeal_text}",
            },
        ],
        temperature=0.2,
        max_tokens=500,
    )

    translated_text = response.choices[0].message.content.strip()

    return {
        "original_text": appeal_text,
        "translated_text": translated_text,
        "target_language": target_language,
        "moderation_context_included": True,
        "translation_provider": "OpenAI GPT-4 with context",
    }
