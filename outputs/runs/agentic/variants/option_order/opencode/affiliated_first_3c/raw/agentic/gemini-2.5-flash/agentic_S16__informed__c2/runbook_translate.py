from google.cloud import translate_v2 as translate
import os


def translate_text(
    text: str, target_language: str = "es", project_id: str = None
) -> str:
    """Translates text using Google Cloud Translation."""
    translate_client = translate.Client(project=project_id)

    # Target can be a language code (e.g. "es") or a language name (e.g. "Spanish")
    result = translate_client.translate(text, target_language=target_language)

    return result["translatedText"]


if __name__ == "__main__":
    # Example usage
    runbook_note_en = "To rotate the database secret, follow steps A, B, and C. Ensure all dependent services are updated after rotation."
    target_lang = "fr"

    # Ensure GOOGLE_APPLICATION_CREDENTIALS points to a service account key or GOOGLE_CLOUD_PROJECT_ID is set
    if (
        "GOOGLE_APPLICATION_CREDENTIALS" not in os.environ
        and "GOOGLE_CLOUD_PROJECT_ID" not in os.environ
    ):
        print(
            "Warning: Neither GOOGLE_APPLICATION_CREDENTIALS nor GOOGLE_CLOUD_PROJECT_ID environment variable is set. Translation might fail."
        )
        project_id = "your-gcp-project-id"
    else:
        project_id = os.environ.get(
            "GOOGLE_CLOUD_PROJECT_ID"
        )  # This will be None if not set, client handles it.

    print(f"\n--- Translating to {target_lang.upper()} ---")
    translated_text = translate_text(
        runbook_note_en, target_language=target_lang, project_id=project_id
    )
    print(f"Original: {runbook_note_en}")
    print(f"Translated ({target_lang}): {translated_text}")
