import os
from google.cloud import translate_v3 as translate

def translate_query(
    project_id: str, 
    query_text: str, 
    target_language_code: str, 
    source_language_code: str = "auto"
) -> str:
    """
    Translates a query text into a target language using Google Cloud Translation API.
    """
    client = translate.TranslationServiceClient()
    
    parent = f"projects/{project_id}/locations/global" # Translation API is global

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [query_text],
            "target_language_code": target_language_code,
            "source_language_code": source_language_code, # 'auto' detects source language
            "mime_type": "text/plain",  # Mime types: "text/plain", "text/html"
        }
    )

    if response.translations:
        return response.translations[0].translated_text
    return query_text # Return original if translation fails

if __name__ == "__main__":
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")

    if not project_id:
        print("Please set the GOOGLE_CLOUD_PROJECT environment variable.")
    else:
        english_query = "How do I get to the nearest train station?"
        spanish_query = "Hola, ¿cómo estás?"
        
        print(f"Original English query: {english_query}")
        translated_to_spanish = translate_query(project_id, english_query, "es")
        print(f"Translated to Spanish: {translated_to_spanish}\n")

        print(f"Original Spanish query: {spanish_query}")
        translated_to_english = translate_query(project_id, spanish_query, "en")
        print(f"Translated to English (auto-detect source): {translated_to_english}\n")

        french_query = "Où sont les toilettes?"
        translated_to_german = translate_query(project_id, french_query, "de")
        print(f"Original French query: {french_query}")
        print(f"Translated to German (auto-detect source): {translated_to_german}\n")