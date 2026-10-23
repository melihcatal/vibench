import os
from google.cloud import translate

def translate_text(text: str, target_language_code: str, project_id: str = None) -> Dict[str, Any]:
    # Google Cloud Translation API documentation:
    # https://cloud.google.com/translate/docs/basic/setup-basic
    
    project_id = project_id or os.getenv("GCP_PROJECT_ID")
    if not project_id:
        raise ValueError("GCP_PROJECT_ID environment variable or project_id parameter must be set.")

    client = translate.TranslationServiceClient()
    location = "global"  # For basic text translation

    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "target_language_code": target_language_code,
        }
    )

    translations = []
    for translation in response.translations:
        translations.append({
            "translated_text": translation.translated_text,
            "detected_language_code": translation.detected_language_code,
        })
    
    return {"translations": translations, "source_text": text, "target_language_code": target_language_code}

if __name__ == '__main__':
    # Example usage (requires GOOGLE_APPLICATION_CREDENTIALS to be set up)
    # translated_output = translate_text("Hello, how are you?", "es", "your-gcp-project-id")
    # print(translated_output)
    # 
    # translated_output_japanese = translate_text("The quick brown fox jumps over the lazy dog.", "ja", "your-gcp-project-id")
    # print(translated_output_japanese)
    pass
