
import os
from google.cloud import translate_v3 as translate

def translate_text(text: str, project_id: str, target_language: str = "en") -> str:
    """Translates text into the target language using Google Cloud Translation."""
    client = translate.TranslationServiceClient()
    location = "global"  # Or specify a region like "us-central1"
    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "target_language_code": target_language,
        }
    )

    translated_text = ""
    for translation in response.translations:
        translated_text += translation.translated_text
    return translated_text

if __name__ == "__main__":
    # Replace with your Google Cloud Project ID
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
    if not project_id:
        print("Please set the GOOGLE_CLOUD_PROJECT_ID environment variable.")
    else:
        transcript_segment = "Hola, ¿cómo estás?"
        target_lang = "en"
        translated_segment = translate_text(transcript_segment, project_id, target_lang)
        print(f"Original: {transcript_segment}")
        print(f"Translated ({target_lang}): {translated_segment}")

        transcript_segment_2 = "J'aime programmer en Python."
        target_lang_2 = "es"
        translated_segment_2 = translate_text(transcript_segment_2, project_id, target_lang_2)
        print(f"Original: {transcript_segment_2}")
        print(f"Translated ({target_lang_2}): {translated_segment_2}")
