from google.cloud import translate


def translate_markup(text, source_lang, target_lang):
    client = translate.TranslationServiceClient()
    response = client.translate_text(
        text, source_language_code=source_lang, target_language_code=target_lang
    )
    return response.translations[0].translated_text


if __name__ == "__main__":
    print(translate_markup("<html><body>Hello, world!</body></html>", "en", "es"))
