import os
from google.cloud import translate_v3 as translate

def translate_text(text: str, target_language_code: str, project_id: str) -> str:
    """
    Translates text to a target language using Google Cloud Translation V3 API.
    Requires GOOGLE_APPLICATION_CREDENTIALS to be set or configured for authentication.
    """
    client = translate.TranslationServiceClient()

    parent = f"projects/{project_id}"
    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "target_language_code": target_language_code,
        }
    )

    # The response contains a list of translations. We take the first one.
    if response.translations:
        return response.translations[0].translated_text
    return text # Return original text if no translation found

if __name__ == '__main__':
    # Example usage (requires GOOGLE_APPLICATION_CREDENTIALS to be set, e.g., via a service account key file)
    # To run:
    # export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/keyfile.json"
    # export GOOGLE_CLOUD_PROJECT_ID="your-gcp-project-id"
    # python multilingual_query_translate.py
    
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
    if not project_id:
        print("Error: GOOGLE_CLOUD_PROJECT_ID environment variable not set.")
        exit(1)

    query_en = "What is the capital of France?"
    query_es = "¿Cuál es la capital de España?"

    print(f"Original English query: {query_en}")
    try:
        translated_query_es = translate_text(query_en, "es", project_id)
        print(f"Translated to Spanish: {translated_query_es}")
    except Exception as e:
        print(f"Error translating English to Spanish: {e}")

    print(f"\nOriginal Spanish query: {query_es}")
    try:
        translated_query_en = translate_text(query_es, "en", project_id)
        print(f"Translated to English: {translated_query_en}")
    except Exception as e:
        print(f"Error translating Spanish to English: {e}")
