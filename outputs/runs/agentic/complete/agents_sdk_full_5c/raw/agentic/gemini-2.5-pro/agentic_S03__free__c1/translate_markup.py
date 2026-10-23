from google.cloud import translate_v2 as translate
from translation_models import SingleTranslation, TranslationResponse


def translate_html_content(request: SingleTranslation) -> TranslationResponse:
    """
    Translates a string containing HTML markup, preserving tags.
    Provider: Google Cloud Translate API
    """
    # Instantiates a client. Assumes GOOGLE_APPLICATION_CREDENTIALS is set.
    translation_client = translate.Client()

    result = translation_client.translate(
        request.text,
        target_language=request.target_language,
        source_language=request.source_language,
        format_='html'  # Provider-specific parameter for handling markup
    )
    
    return TranslationResponse(
        translated_text=result['translatedText'],
        detected_source_language=result.get('detectedSourceLanguage', '')
    )
