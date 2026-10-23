import os
from typing import List
from translation_client import get_translation_client
from translation_models import TranslationRequest, TranslationResponse
from google.cloud.translate_v3 import TranslateTextRequest

def batch_translate_texts(requests: List[TranslationRequest]) -> List[TranslationResponse]:
    client = get_translation_client()
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
    parent = f"projects/{project_id}"

    contents = [req.text for req in requests]
    if not contents:
        return []

    # Assuming all requests have the same source and target languages for a batch
    source_language = requests[0].source_language
    target_language = requests[0].target_language

    translation_request = TranslateTextRequest(
        parent=parent,
        contents=contents,
        source_language_code=source_language,
        target_language_code=target_language,
    )

    response = client.translate_text(request=translation_request)
    
    translated_responses = [
        TranslationResponse(translated_text=t.translated_text)
        for t in response.translations
    ]
    return translated_responses
