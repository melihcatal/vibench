from typing import Optional
from openai import OpenAI
from model_client import get_llm_client
from model_models import normalize_model_response


def translate_text(
    text: str, target_language: str, source_language: Optional[str] = None
) -> str:
    """
    Translate text using a hosted LLM.

    Args:
        text: Text to translate
        target_language: Target language code (e.g., 'es', 'fr', 'de')
        source_language: Optional source language code

    Returns:
        Translated text
    """
    client = get_llm_client()

    language_names = {
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
    }

    target_lang_name = language_names.get(target_language.lower(), target_language)

    if source_language:
        source_lang_name = language_names.get(source_language.lower(), source_language)
        prompt = f"Translate the following text from {source_lang_name} to {target_lang_name}:\n\n{text}"
    else:
        prompt = f"Translate the following text to {target_lang_name}:\n\n{text}"

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "You are a professional translator. Provide accurate translations.",
                },
                {"role": "user", "content": prompt},
            ],
            max_tokens=1000,
            temperature=0.3,
        )

        translated = response.choices[0].message.content.strip()

        return translated

    except Exception as e:
        raise Exception(f"Failed to translate text: {str(e)}")


def translate_model_output(output_text: str, target_language: str) -> dict:
    """
    Translate model-generated output to another language.

    Args:
        output_text: Model-generated text to translate
        target_language: Target language code

    Returns:
        Dictionary with translation results
    """
    translated = translate_text(output_text, target_language)

    return {
        "original_text": output_text,
        "translated_text": translated,
        "target_language": target_language,
        "model_used": "gpt-4o",
        "provider": "openai",
    }


def batch_translate(texts: list, target_language: str) -> list:
    """
    Translate multiple texts in batch.

    Args:
        texts: List of texts to translate
        target_language: Target language code

    Returns:
        List of translated texts
    """
    results = []

    for text in texts:
        try:
            translated = translate_text(text, target_language)
            results.append(translated)
        except Exception as e:
            results.append(f"[Translation failed: {str(e)}]")

    return results


def detect_language(text: str) -> str:
    """
    Detect the language of text using a hosted LLM.

    Args:
        text: Text to analyze

    Returns:
        Detected language code
    """
    client = get_llm_client()

    prompt = f"Detect the language of the following text and return only the ISO 639-1 language code (e.g., 'en', 'es', 'fr'):\n\n{text}"

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a language detection expert. Return only the ISO 639-1 language code.",
                },
                {"role": "user", "content": prompt},
            ],
            max_tokens=10,
            temperature=0.1,
        )

        detected = response.choices[0].message.content.strip().lower()

        # Clean up response
        detected = detected.replace('"', "").replace("'", "").strip()

        return detected

    except Exception as e:
        raise Exception(f"Failed to detect language: {str(e)}")
