from google.cloud import translate_v3
from typing import List, Dict

def translate_dashboard_notes(project_id: str, contents: List[str], target_language_code: str,
                              source_language_code: str = None) -> Dict[str, str]:
    client = translate_v3.TranslationServiceClient()
    parent = f"projects/{project_id}/locations/global"

    translated_notes = {}

    for content in contents:
        request = {
            "parent": parent,
            "contents": [content],
            "target_language_code": target_language_code,
        }
        if source_language_code:
            request["source_language_code"] = source_language_code

        response = client.translate_text(request=request)

        for translation in response.translations:
            translated_notes[content] = translation.translated_text
            
    return translated_notes