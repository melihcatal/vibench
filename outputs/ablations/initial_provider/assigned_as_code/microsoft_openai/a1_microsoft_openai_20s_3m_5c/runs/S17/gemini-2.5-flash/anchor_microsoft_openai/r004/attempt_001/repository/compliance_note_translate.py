from google.cloud import translate_v3 as translate
import os
from typing import List, Dict, Any

def translate_compliance_notes(texts: List[str], target_language_code: str, project_id: str) -> List[Dict[str, Any]]:

    client = translate.TranslationServiceClient()

    parent = f"projects/{project_id}/locations/global"

    translations_results = []
    for text in texts:
        try:
            response = client.translate_text(
                request={
                    "parent": parent,
                    "contents": [text],
                    "target_language_code": target_language_code,
                }
            )

            translated_text = response.translations[0].translated_text
            detected_source_language = response.translations[0].detected_language_code

            translations_results.append({
                "original_text": text,
                "translated_text": translated_text,
                "detected_source_language": detected_source_language
            })
        except Exception as e:
            print(f"Error translating text '{text}': {e}")
            translations_results.append({"original_text": text, "translated_text": None, "error": str(e)})

    return translations_results
