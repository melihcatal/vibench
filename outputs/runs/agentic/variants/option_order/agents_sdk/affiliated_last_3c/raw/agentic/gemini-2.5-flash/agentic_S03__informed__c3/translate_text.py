import os
from google.cloud import translate_v2 as translate

from translation_client import get_translate_client
from translation_models import TranslationRequest, TranslationResponse

def translate_text(request: TranslationRequest) -> TranslationResponse:
    """Translates a single text string using Google Cloud Translation."""
    client = get_translate_client()
    
    result = client.translate(
        request.text,
        target_language=request.target_language,
        source_language=request.source_language,
        format_=(request.format or 'text')
    )

    translated_text = result['translatedText']
    detected_source_language = result['detectedSourceLanguage']

    return TranslationResponse(
        translated_text=translated_text,
        source_language=detected_source_language,
        target_language=request.target_language
    )

if __name__ == '__main__':
    # Example usage for testing
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/path/to/your/google_credentials.json' # Replace with actual path
    
    # Simple text translation
    request = TranslationRequest(text="Hello, world!", target_language="es")
    response = translate_text(request)
    print(f"Original: {request.text}, Translated: {response.translated_text}, Source: {response.source_language}")

    # HTML translation
    html_request = TranslationRequest(text="<h1>Hello, world!</h1>", target_language="fr", format="html")
    html_response = translate_text(html_request)
    print(f"Original HTML: {html_request.text}, Translated HTML: {html_response.translated_text}, Source: {html_response.source_language}")
