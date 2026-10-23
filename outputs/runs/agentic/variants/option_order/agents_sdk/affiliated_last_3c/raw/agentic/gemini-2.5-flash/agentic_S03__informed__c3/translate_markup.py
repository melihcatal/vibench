import os
from google.cloud import translate_v2 as translate

from translation_client import get_translate_client
from translation_models import TranslationRequest, TranslationResponse

def translate_markup(request: TranslationRequest) -> TranslationResponse:
    """Translates HTML or markup using Google Cloud Translation while preserving tags."""
    client = get_translate_client()
    
    # Ensure the format is set to 'html' for markup translation
    result = client.translate(
        request.text,
        target_language=request.target_language,
        source_language=request.source_language,
        format='html' # Explicitly set format to html
    )

    translated_text = result['translatedText']
    detected_source_language = result['detectedSourceLanguage']

    return TranslationResponse(
        translated_text=translated_text,
        source_language=detected_source_language,
        target_language=request.target_language,
        original_text=request.text
    )

if __name__ == '__main__':
    # Example usage for testing
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/path/to/your/google_credentials.json' # Replace with actual path
    
    html_content = """<!DOCTYPE html><html><body><h1>Welcome!</h1><p>This is a paragraph.</p></body></html>"""
    request = TranslationRequest(text=html_content, target_language="fr")
    response = translate_markup(request)
    print(f"Original HTML: {request.text}\nTranslated HTML: {response.translated_text}\nSource: {response.source_language}")

    # Example with simple HTML snippet
    div_content = "<div><span>Hello</span> <b>World</b>!</div>"
    div_request = TranslationRequest(text=div_content, target_language="es")
    div_response = translate_markup(div_request)
    print(f"Original HTML: {div_request.text}\nTranslated HTML: {div_response.translated_text}\nSource: {div_response.source_language}")
