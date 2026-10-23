from vision_client import VisionClient
from vision_models import ImageDescriptionResponse, TranslatedText

def translate_alt_text(
    description_response: ImageDescriptionResponse, 
    target_language: str = "en"
) -> TranslatedText:
    client = VisionClient()
    google_translate_client = client.get_google_translate_client()

    if not description_response.description:
        return TranslatedText(translated_description="", source_language="", target_language=target_language)

    result = google_translate_client.translate(
        description_response.description,
        target_language=target_language
    )

    translated_description = result['translatedText']
    source_language = result['detectedSourceLanguage']

    return TranslatedText(
        translated_description=translated_description,
        source_language=source_language,
        target_language=target_language
    )