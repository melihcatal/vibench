from typing import List
from google.cloud import translate_v2 as translate
from translation_models import BatchTranslation


def translate_batch(request: BatchTranslation) -> List[dict]:
    """
    Translates a list of strings using Google Cloud Translate, preserving order.
    """
    # Instantiates a client. Assumes GOOGLE_APPLICATION_CREDENTIALS is set.
    translation_client = translate.Client()
    
    # The Google Cloud Translate API returns a list of dictionaries in the same
    # order as the input list.
    results = translation_client.translate(
        request.texts,
        target_language=request.target_language,
        source_language=request.source_language
    )
    return results
