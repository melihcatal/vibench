import os
from google.cloud import translate_v3 as translate

def translate_compliance_note(text: str, target_language_code: str, project_id: str, source_language_code: str = None) -> str:
    """
    Translates encryption or compliance notes for reviewers using Google Cloud Translation.
    """
    translate_client = translate.TranslationServiceClient()

    parent = f"projects/{project_id}/locations/global"

    response = translate_client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "target_language_code": target_language_code,
            "source_language_code": source_language_code, # Optional: Google can often auto-detect
        }
    )

    # The 'translations' list will contain one entry for each text provided in 'contents'
    if response.translations:
        return response.translations[0].translated_text
    return ""
