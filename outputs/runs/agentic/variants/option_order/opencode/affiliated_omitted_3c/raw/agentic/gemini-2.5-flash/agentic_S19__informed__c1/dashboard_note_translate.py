import observability_client


def translate_dashboard_note(text: str, target_lang: str = "en") -> str:
    translator = observability_client.get_deepl_translator()

    # DeepL API supports target languages like 'en', 'es', 'fr', etc.
    # The source_lang parameter can be omitted for auto-detection.
    result = translator.translate_text(text, target_lang=target_lang)

    return result.text
