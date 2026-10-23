import os
from google.cloud import translate_v2 as translate
from typing import List, Dict

def translate_query_for_multilingual_search(query: str, target_language: str, project_id: str) -> str:
    translate_client = translate.Client(project=project_id)
    
    result = translate_client.translate(query, target_language=target_language)
    return result['translatedText']