import os
from google.cloud import translate_v2 as translate
from typing import List, Dict, Any

def translate_text_fields(texts: List[str], target_language: str, project_id: str) -> List[Dict[str, Any]]:
    """
    Translates user-facing document fields using Google Cloud Translation.
    Requires GOOGLE_APPLICATION_CREDENTIALS to be set in the environment.
    """
    translate_client = translate.Client(project=project_id)

    translations = []
    for text in texts:
        result = translate_client.translate(
            text,
            target_language=target_language
        )
        translations.append({
            "input": text,
            "translatedText": result['translatedText'],
            "detectedSourceLanguage": result['detectedSourceLanguage']
        })
    return translations

if __name__ == "__main__":
    # Example usage (requires GOOGLE_APPLICATION_CREDENTIALS env var and a Google Cloud project ID)
    texts_to_translate = [
        "Hello, world!",
        "This is a test sentence."
    ]
    target_lang = "es"
    gcp_project_id = os.environ.get("GOOGLE_CLOUD_PROJECT") # Or your actual project ID

    if gcp_project_id:
        # translated_results = translate_text_fields(texts_to_translate, target_lang, gcp_project_id)
        # for res in translated_results:
        #     print(f"Original: {res['input']}, Translated ({res['detectedSourceLanguage']}->{target_lang}): {res['translatedText']}")
        print("To run this example, ensure GOOGLE_APPLICATION_CREDENTIALS and GOOGLE_CLOUD_PROJECT are set and uncomment the example usage.")
    else:
        print("Please set the GOOGLE_CLOUD_PROJECT environment variable.")
