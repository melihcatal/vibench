from safety_client import aws_comprehend_client


def appeal_translate(text: str, source_language: str = "auto", target_language: str = "en") -> str:
    client = aws_comprehend_client("translate")
    response = client.translate_text(Text=text, SourceLanguageCode=source_language, TargetLanguageCode=target_language)
    return response.get("TranslatedText", text)
