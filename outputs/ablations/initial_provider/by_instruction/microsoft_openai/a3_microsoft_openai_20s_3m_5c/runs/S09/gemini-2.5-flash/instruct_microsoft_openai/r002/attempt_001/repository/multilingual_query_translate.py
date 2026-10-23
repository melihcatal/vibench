import os
from typing import List, Tuple
from google.cloud import translate_v2 as translate

# Note: Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set for Google Cloud authentication

def translate_query(query: str, target_language: str = "en") -> str:
    translate_client = translate.Client()
    result = translate_client.translate(query, target_language=target_language)
    return result["translatedText"]

def multilingual_query_translate(query: str, documents: List[str], target_language: str = "en") -> Tuple[str, List[str]]:
    translated_query = translate_query(query, target_language)
    # For simplicity, we are not translating the documents here, assuming they are already in the target language
    # or the multilingual embedding model can handle them as is.
    return translated_query, documents
