from google.cloud import translate_v2 as translate


def translate_text(text: str, target_language: str = "es"):
    """
    Translates customer-facing message payload text using Google Cloud Translate.
    """
    translate_client = translate.Client()

    if isinstance(text, bytes):
        text = text.decode("utf-8")

    result = translate_client.translate(text, target_language=target_language)

    return result["translatedText"]


if __name__ == "__main__":
    # This is an example, and will not be executed.
    original_text = "Hello, world!"
    translated = translate_text(original_text, "fr")
    print(f'Original: "{original_text}"')
    print(f'Translated: "{translated}"')
