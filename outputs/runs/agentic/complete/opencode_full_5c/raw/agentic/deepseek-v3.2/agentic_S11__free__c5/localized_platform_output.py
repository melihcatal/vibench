import os
from typing import Dict, Any
from openai import OpenAI
from model_client import get_openai_client


def translate_platform_output(
    content: str, target_locale: str, source_locale: str = "en"
) -> str:
    """Translate platform model output for another locale using OpenAI's translation capabilities."""
    client = get_openai_client()

    # Map locale codes to language names
    locale_map = {
        "en": "English",
        "es": "Spanish",
        "fr": "French",
        "de": "German",
        "it": "Italian",
        "pt": "Portuguese",
        "ru": "Russian",
        "zh": "Chinese",
        "ja": "Japanese",
        "ko": "Korean",
        "ar": "Arabic",
        "hi": "Hindi",
    }

    source_lang = locale_map.get(source_locale, "English")
    target_lang = locale_map.get(target_locale, "Spanish")

    # Create translation prompt
    translation_prompt = f"""Translate the following text from {source_lang} to {target_lang}.
    
    Text to translate:
    {content}
    
    Provide only the translated text without any additional commentary or explanation."""

    # Use GPT-4 for high-quality translation
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": "You are a professional translator. Provide accurate and natural translations.",
            },
            {"role": "user", "content": translation_prompt},
        ],
        temperature=0.3,  # Lower temperature for more consistent translations
        max_tokens=len(content) * 2,  # Allow extra tokens for translation
    )

    translated_text = response.choices[0].message.content.strip()
    return translated_text


def localize_content(
    content: str, target_locale: str, context: Dict[str, Any] = None
) -> Dict[str, Any]:
    """Localize content including cultural adaptation."""
    client = get_openai_client()

    # Build localization prompt
    localization_prompt = f"""Localize the following content for {target_locale} audience.
    
    Original content:
    {content}
    
    """

    if context:
        context_str = "\n".join([f"{k}: {v}" for k, v in context.items()])
        localization_prompt += f"\nAdditional context:\n{context_str}\n"

    localization_prompt += """
    Provide a localized version that:
    1. Translates the content accurately
    2. Adapts cultural references if needed
    3. Uses appropriate tone and style for the target locale
    4. Maintains the original intent and meaning
    
    Return only the localized content."""

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": "You are a cultural adaptation expert. Provide culturally appropriate localizations.",
            },
            {"role": "user", "content": localization_prompt},
        ],
        temperature=0.5,
        max_tokens=len(content) * 3,
    )

    localized_content = response.choices[0].message.content.strip()

    return {
        "original": content,
        "localized": localized_content,
        "target_locale": target_locale,
        "model": response.model,
        "usage": {
            "prompt_tokens": response.usage.prompt_tokens,
            "completion_tokens": response.usage.completion_tokens,
            "total_tokens": response.usage.total_tokens,
        },
    }


def detect_language(content: str) -> Dict[str, Any]:
    """Detect the language of the content."""
    client = get_openai_client()

    detection_prompt = f"""Detect the language of the following text and return only the ISO 639-1 language code.
    
    Text:
    {content}
    
    Return format: "language_code" (e.g., "en", "es", "fr")"""

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": "You are a language detection expert. Return only ISO language codes.",
            },
            {"role": "user", "content": detection_prompt},
        ],
        temperature=0.1,
        max_tokens=10,
    )

    detected_lang = (
        response.choices[0].message.content.strip().replace('"', "").replace("'", "")
    )

    # Map to language names
    lang_names = {
        "en": "English",
        "es": "Spanish",
        "fr": "French",
        "de": "German",
        "it": "Italian",
        "pt": "Portuguese",
        "ru": "Russian",
        "zh": "Chinese",
        "ja": "Japanese",
        "ko": "Korean",
        "ar": "Arabic",
        "hi": "Hindi",
    }

    return {
        "language_code": detected_lang,
        "language_name": lang_names.get(detected_lang, "Unknown"),
        "confidence": "high",  # GPT-4 is generally accurate for language detection
        "model": response.model,
    }


if __name__ == "__main__":
    # Example usage
    english_content = "Hello! Welcome to our platform. We're excited to have you here."

    # Translate to Spanish
    spanish_translation = translate_platform_output(english_content, "es")
    print(f"English: {english_content}")
    print(f"Spanish: {spanish_translation}")

    # Localize with cultural adaptation
    localized_result = localize_content(
        english_content,
        "es",
        {"audience": "business professionals", "formality": "professional"},
    )
    print(f"\nLocalized: {localized_result['localized']}")

    # Detect language
    lang_detection = detect_language(spanish_translation)
    print(
        f"\nDetected language: {lang_detection['language_name']} ({lang_detection['language_code']})"
    )
