import boto3


def translate_text(
    text: str,
    target_language_code: str,
    source_language_code: str = "auto",
) -> str:
    """
    Translates text using Amazon Translate.

    :param text: The text to translate.
    :param target_language_code: The ISO 639-1 code for the target language.
    :param source_language_code: The ISO 639-1 code for the source language. 'auto' for auto-detection.
    :return: The translated text.
    """
    translate_client = boto3.client("translate")

    try:
        response = translate_client.translate_text(
            Text=text,
            SourceLanguageCode=source_language_code,
            TargetLanguageCode=target_language_code,
        )
        return response.get("TranslatedText", "")
    except Exception as e:
        print(f"An error occurred during translation: {e}")
        return f"Error: Could not translate text."
