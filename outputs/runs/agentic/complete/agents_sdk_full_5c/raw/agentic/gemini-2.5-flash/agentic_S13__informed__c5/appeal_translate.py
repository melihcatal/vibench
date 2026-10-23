import os
from google.cloud import translate_v3 as translate
from typing import List

def appeal_translate(texts: List[str], target_language: str = "en", project_id: str = None) -> List[str]:
    """
    Translates appeal text for review using Google Cloud Translation.
    """
    if not project_id:
        project_id = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
    
    if not project_id:
        raise ValueError("Google Cloud Project ID not provided and GOOGLE_CLOUD_PROJECT_ID environment variable not set.")

    client = translate.TranslationServiceClient()
    parent = f"projects/{project_id}/locations/global"

    translations = []
    for text in texts:
        response = client.translate_text(
            request={
                "parent": parent,
                "contents": [text],
                "target_language_code": target_language,
            }
        )
        for translation in response.translations:
            translations.append(translation.translated_text)
    
    return translations

if __name__ == '__main__':
    # Example usage (requires GOOGLE_APPLICATION_CREDENTIALS or gcloud auth to be configured,
    # and GOOGLE_CLOUD_PROJECT_ID environment variable to be set)
    # appeal_texts = [
    #     "Je voudrais faire appel de cette décision.",
    #     "Dieser Inhalt wurde fälschlicherweise markiert."
    # ]
    # translated_texts = appeal_translate(appeal_texts, target_language="en")
    # print(translated_texts)
    pass
