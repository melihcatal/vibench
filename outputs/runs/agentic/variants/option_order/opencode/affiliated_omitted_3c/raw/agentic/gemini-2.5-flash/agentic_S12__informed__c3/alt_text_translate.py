from vision_client import VisionClient


def translate_alt_text(text: str, target_language_code: str = "es") -> str:
    translate_client = VisionClient().get_translate_client()
    response = translate_client.translate_text(
        Text=text, SourceLanguageCode="en", TargetLanguageCode=target_language_code
    )
    return response.get("TranslatedText", text)
