from translation_client import TranslationClient


def alt_text_translate(text: str, target_language_code: str = "es") -> str:
    translate_client = TranslationClient()
    client = translate_client.get_client()
    parent = translate_client.get_parent()

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "target_language_code": target_language_code,
        }
    )

    translations = [
        translation.translated_text for translation in response.translations
    ]
    return translations[0] if translations else ""
