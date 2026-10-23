import os
from google.cloud import translate_v2 as translate


def translate_narration_script(text, target_language="en", source_language=None):
    """Translate narration scripts before synthesis using Google Cloud Translation."""
    client = translate.Client()

    if isinstance(text, bytes):
        text = text.decode("utf-8")

    result = client.translate(
        text,
        target_language=target_language,
        source_language=source_language,
        format_="text",
    )

    return {
        "translated_text": result["translatedText"],
        "detected_source_language": result.get("detectedSourceLanguage"),
        "original_text": text,
    }


def translate_batch_narrations(texts, target_language="en"):
    """Translate multiple narration scripts in batch."""
    client = translate.Client()

    results = client.translate(texts, target_language=target_language, format_="text")

    translations = []
    for i, result in enumerate(results):
        translations.append(
            {
                "original": texts[i],
                "translated": result["translatedText"],
                "detected_language": result.get("detectedSourceLanguage"),
            }
        )

    return translations


def translate_with_glossary(text, target_language="en", glossary_id=None):
    """Translate with custom glossary for domain-specific terms."""
    from google.cloud import translate_v3beta1 as translate_v3

    client = translate_v3.TranslationServiceClient()

    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    location = "us-central1"

    parent = f"projects/{project_id}/locations/{location}"

    glossary_config = None
    if glossary_id:
        glossary_config = translate_v3.TranslateTextGlossaryConfig(
            glossary=f"{parent}/glossaries/{glossary_id}"
        )

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "target_language_code": target_language,
            "glossary_config": glossary_config,
        }
    )

    return response.translations[0].translated_text
