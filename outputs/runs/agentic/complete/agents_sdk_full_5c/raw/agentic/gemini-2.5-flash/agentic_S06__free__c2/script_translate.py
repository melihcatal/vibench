from google.cloud import translate

def script_translate(text: str, target_language_code: str, source_language_code: str = None) -> str:
    client = translate.TranslationServiceClient()
    location = "global" # For most general-purpose translation
    parent = f"projects/{{client.project}}/locations/{location}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",  # Can be "text/plain" or "text/html"
            "source_language_code": source_language_code,
            "target_language_code": target_language_code,
        }
    )

    # The response can contain multiple translations, but we only send one text.
    for translation in response.translations:
        return translation.translated_text
    return text # Return original text if no translation found

if __name__ == '__main__':
    # Example usage (requires credentials)
    original_text = "Hello, how are you?"
    translated_text_es = script_translate(original_text, "es")
    print(f"Original (en): {original_text}")
    print(f"Translated (es): {translated_text_es}")

    original_text_ja = "こんにちは、お元気ですか？"
    translated_text_en = script_translate(original_text_ja, "en", source_language_code="ja")
    print(f"Original (ja): {original_text_ja}")
    print(f"Translated (en): {translated_text_en}")
