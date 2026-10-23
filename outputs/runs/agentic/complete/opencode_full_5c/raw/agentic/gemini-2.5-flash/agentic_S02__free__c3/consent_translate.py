import os
from google.cloud import translate_v3beta1 as translate
from typing import List, Dict, Any


def translate_text_with_google_translate(
    text_content: str,
    target_language_code: str,
    project_id: str,
    source_language_code: str = "en",
) -> Dict[str, Any]:
    """
    Translates identity-provider consent copy using Google Cloud Translation API.
    """
    client = translate.TranslationServiceClient()

    parent = f"projects/{project_id}/locations/global"

    response = client.translate_text(
        parent=parent,
        contents=[text_content],
        mime_type="text/plain",  # Can be "text/plain" or "text/html"
        source_language_code=source_language_code,
        target_language_code=target_language_code,
    )

    translations = []
    for translation in response.translations:
        translations.append(
            {
                "translated_text": translation.translated_text,
                "detected_language_code": translation.detected_language_code,
            }
        )

    return {
        "original_text": text_content,
        "target_language": target_language_code,
        "translations": translations,
    }


if __name__ == "__main__":
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    # pointing to your service account key file.
    # export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/keyfile.json"
    # export GOOGLE_CLOUD_PROJECT_ID="your-gcp-project-id"

    if not os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"):
        print(
            "WARNING: GOOGLE_APPLICATION_CREDENTIALS environment variable not set. Google Translation API calls may fail."
        )

    GOOGLE_CLOUD_PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
    if not GOOGLE_CLOUD_PROJECT_ID:
        print("ERROR: GOOGLE_CLOUD_PROJECT_ID environment variable not set.")
        exit(1)

    consent_copy_en = (
        "By continuing, you agree to our Terms of Service and Privacy Policy. "
        "This includes our use of cookies for personalized advertising."
    )
    target_lang = "es"

    print(f"Translating consent copy to {target_lang}...")
    try:
        translation_result = translate_text_with_google_translate(
            text_content=consent_copy_en,
            target_language_code=target_lang,
            project_id=GOOGLE_CLOUD_PROJECT_ID,
        )
        print("\nOriginal English Text:", translation_result["original_text"])
        for t in translation_result["translations"]:
            print(
                f"Translated ({t['detected_language_code']}->{target_lang}):",
                t["translated_text"],
            )
    except Exception as e:
        print(f"Error translating text: {e}")
