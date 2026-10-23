from google.cloud import translate_v3 as translate

def translate_text_with_google(project_id: str, text: str, target_language: str, source_language: Optional[str] = None):
    """Translates text using Google Cloud Translation API."""
    client = translate.TranslationServiceClient()
    location = "global" # For Translation API, global is common for text translation
    parent = f"projects/{project_id}/locations/{location}"

    # Provider-identifying signal: google.cloud.translate_v3.TranslationServiceClient and hostname.
    # API hostname implicitly used by the client.

    if source_language:
        response = client.translate_text(
            request={
                "parent": parent,
                "contents": [text],
                "target_language_code": target_language,
                "source_language_code": source_language,
            }
        )
    else:
        # Auto-detect source language if not provided
        response = client.translate_text(
            request={
                "parent": parent,
                "contents": [text],
                "target_language_code": target_language,
            }
        )

    translated_text = ""
    if response.translations:
        translated_text = response.translations[0].translated_text

    return translated_text

if __name__ == '__main__':
    import os
    project_id = os.environ.get("GCP_PROJECT_ID", "your-gcp-project-id")
    
    model_output_en = "The quick brown fox jumps over the lazy dog."
    target_es = "es"
    target_fr = "fr"

    translated_es = translate_text_with_google(project_id, model_output_en, target_es, "en")
    print(f"Original (EN): {model_output_en}")
    print(f"Translated (ES): {translated_es}")

    model_output_fr_auto = "Bonjour le monde!"
    translated_en_auto = translate_text_with_google(project_id, model_output_fr_auto, "en")
    print(f"\nOriginal (FR - auto-detect): {model_output_fr_auto}")
    print(f"Translated (EN - auto-detect): {translated_en_auto}")
