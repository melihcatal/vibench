import os
from typing import List
from google.cloud import translate_v2 as translate

from translation_client import get_translate_client
from translation_models import BatchTranslationRequest, TranslationResponse

def batch_translate(request: BatchTranslationRequest) -> List[TranslationResponse]:
    """Translates a list of text strings using Google Cloud Translation while preserving order."""
    client = get_translate_client()
    
    # The Google Cloud Translate API can translate multiple texts in one call
    results = client.translate(
        request.texts,
        target_language=request.target_language,
        source_language=request.source_language,
        format_=(request.format or 'text')
    )

    responses = []
    for i, result in enumerate(results):
        translated_text = result['translatedText']
        detected_source_language = result['detectedSourceLanguage']
        responses.append(TranslationResponse(
            translated_text=translated_text,
            source_language=detected_source_language,
            target_language=request.target_language,
            original_text=request.texts[i]
        ))
    
    return responses

if __name__ == '__main__':
    # Example usage for testing
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/path/to/your/google_credentials.json' # Replace with actual path

    request = BatchTranslationRequest(
        texts=["Hello, world!", "How are you?"],
        target_language="es"
    )
    responses = batch_translate(request)
    for resp in responses:
        print(f"Original: {resp.original_text}, Translated: {resp.translated_text}, Source: {resp.source_language}")

    html_request = BatchTranslationRequest(
        texts=["<p>Hello</p>", "<div>World</div>"],
        target_language="fr",
        format="html"
    )
    html_responses = batch_translate(html_request)
    for resp in html_responses:
        print(f"Original HTML: {resp.original_text}, Translated HTML: {resp.translated_text}, Source: {resp.source_language}")
