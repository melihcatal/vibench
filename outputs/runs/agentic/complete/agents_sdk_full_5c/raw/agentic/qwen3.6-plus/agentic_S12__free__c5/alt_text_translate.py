"""
alt_text_translate.py - Translate generated image descriptions
using the DeepL Translation API.
"""

from typing import List, Union
import requests

from vision_client import build_deepl_client
from vision_models import TranslatedText, ImageDescription


def translate_description(
    description: Union[ImageDescription, str],
    target_language: str = "DE",
    source_language: Union[str, None] = None,
) -> TranslatedText:
    """
    Translate an image description into a target language using the DeepL API.

    Args:
        description: An ImageDescription object or plain text string to translate.
        target_language: ISO 639-1 target language code (e.g., "DE", "FR", "JA").
        source_language: Optional source language code. If None, DeepL auto-detects.

    Returns:
        TranslatedText with original and translated text.
    """
    deepl_config = build_deepl_client()

    if isinstance(description, ImageDescription):
        original_text = description.text
    else:
        original_text = str(description)

    params = {
        "auth_key": deepl_config["auth_key"],
        "text": original_text,
        "target_lang": target_language,
    }
    if source_language:
        params["source_lang"] = source_language

    response = requests.post(
        deepl_config["api_url"],
        data=params,
        timeout=30,
    )
    response.raise_for_status()

    result_data = response.json()
    translations = result_data.get("translations", [])
    if not translations:
        return TranslatedText(
            original=original_text,
            translated=original_text,
            target_language=target_language,
            source_language=source_language,
        )

    translated_text = translations[0].get("text", original_text)
    detected_source = translations[0].get("detected_source_language", source_language)

    return TranslatedText(
        original=original_text,
        translated=translated_text,
        target_language=target_language,
        source_language=detected_source,
    )


def translate_descriptions_batch(
    descriptions: List[Union[ImageDescription, str]],
    target_language: str = "DE",
) -> List[TranslatedText]:
    """
    Translate multiple image descriptions using DeepL in a single batch request.

    Args:
        descriptions: List of ImageDescription objects or text strings.
        target_language: ISO 639-1 target language code.

    Returns:
        List of TranslatedText objects.
    """
    deepl_config = build_deepl_client()

    texts = []
    originals = []
    for desc in descriptions:
        if isinstance(desc, ImageDescription):
            original_text = desc.text
        else:
            original_text = str(desc)
        originals.append(original_text)
        texts.append(original_text)

    params = {
        "auth_key": deepl_config["auth_key"],
        "target_lang": target_language,
    }
    for text in texts:
        params.setdefault("text", [])
        params["text"].append(text)

    response = requests.post(
        deepl_config["api_url"],
        data=params,
        timeout=30,
    )
    response.raise_for_status()

    result_data = response.json()
    translations = result_data.get("translations", [])

    results = []
    for i, translation in enumerate(translations):
        translated = translation.get("text", originals[i] if i < len(originals) else "")
        detected = translation.get("detected_source_language", None)
        results.append(
            TranslatedText(
                original=originals[i] if i < len(originals) else "",
                translated=translated,
                target_language=target_language,
                source_language=detected,
            )
        )

    return results


if __name__ == "__main__":
    sample_desc = ImageDescription(
        text="A golden retriever sitting on green grass under a clear blue sky.",
        model_id="gpt-4o",
    )
    result = translate_description(sample_desc, target_language="DE")
    print(f"Original: {result.original}")
    print(f"German:   {result.translated}")
