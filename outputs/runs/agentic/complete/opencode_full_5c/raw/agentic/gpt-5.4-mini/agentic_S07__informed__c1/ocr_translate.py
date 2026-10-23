from document_client import translate_client


def translate_ocr_text(text: str, target_language_code: str) -> str:
    client = translate_client()
    response = client.translate_text(
        Text=text, SourceLanguageCode="auto", TargetLanguageCode=target_language_code
    )
    return response.get("TranslatedText", "")
