from google.cloud import translate_v3 as translate
import os


if __name__ == "__main__":
    text = os.getenv("LOG_TEXT", "")
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT") or os.getenv("GCP_PROJECT") or os.getenv("GOOGLE_PROJECT_ID")
    target_language = os.getenv("TARGET_LANGUAGE", "es")
    if not project_id:
        raise ValueError("Missing Google Cloud project id")
    client = translate.TranslationServiceClient()
    parent = f"projects/{project_id}/locations/global"
    response = client.translate_text(contents=[text], target_language_code=target_language, parent=parent)
    translated = response.translations[0].translated_text if response.translations else ""
    print(translated)
