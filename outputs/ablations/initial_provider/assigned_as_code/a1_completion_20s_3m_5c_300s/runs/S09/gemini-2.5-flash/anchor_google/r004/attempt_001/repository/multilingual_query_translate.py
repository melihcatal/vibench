import os
from typing import List, Dict
from google.cloud import translate_v2 as translate
from embeddings_models import GOOGLE_TRANSLATE_LOCATION

def multilingual_query_translate(payload: Dict, config: Dict = None) -> Dict:
    config = config or {}
    # Google Cloud Translation API typically uses application default credentials
    # or GOOGLE_APPLICATION_CREDENTIALS environment variable.
    # No explicit API key is usually passed here for server-side auth.

    translate_client = translate.Client(project=os.environ.get("GOOGLE_CLOUD_PROJECT"))

    query_text = payload.get("query")
    target_language = payload.get("target_language")

    if not isinstance(query_text, str):
        raise ValueError("Payload must contain a 'query' key with a string.")
    if not isinstance(target_language, str) or not target_language:
        raise ValueError("Payload must contain a 'target_language' key with a string (e.g., 'es', 'fr').")

    try:
        # The target_language parameter is required
        response = translate_client.translate(query_text, target_language=target_language)
        translated_query = response["translatedText"]
        source_language = response["detectedSourceLanguage"]
    except Exception as e:
        translated_query = None
        source_language = None
        print(f"Error during translation: {e}") # For debugging, not for return

    return {
        "original_query": query_text,
        "target_language": target_language,
        "translated_query": translated_query,
        "detected_source_language": source_language,
    }
