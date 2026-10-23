from google.cloud import translate_v2 as translate
import os


def translate_log_message(
    text: str, target_language_code: str, project_id: str = None
) -> str:
    """Translates a log message to a target locale using Google Cloud Translation API.

    Args:
        text: The log message text to translate.
        target_language_code: The BCP-47 language code for the target language (e.g., 'es' for Spanish).
        project_id: The GCP project ID. If None, it will be inferred from the environment.

    Returns:
        The translated text.
    """
    if not text:
        return ""

    # Google Cloud Translation client - Provider-identifying signal: translate.Client()
    translate_client = (
        translate.Client(project=project_id) if project_id else translate.Client()
    )

    # The target language must be a BCP-47 language code.
    result = translate_client.translate(text, target_language=target_language_code)

    translated_text = result["translatedText"]
    # The source language is automatically detected, but can be specified if known.
    # print(f"Detected source language: {result['detectedSourceLanguage']}")

    return translated_text


if __name__ == "__main__":
    # Example Usage (requires GCP_PROJECT_ID env var)
    project_id = os.getenv("GCP_PROJECT_ID")
    if not project_id:
        print("Please set the GCP_PROJECT_ID environment variable to run this example.")
    else:
        english_message = (
            "Failed to connect to the database. Please check network connectivity."
        )
        spanish_translation = translate_log_message(
            english_message, "es", project_id=project_id
        )
        print(f"\nEnglish: {english_message}")
        print(f"Spanish: {spanish_translation}")

        french_message = "Utilisateur non autorisé: Accès refusé à la ressource."
        english_translation = translate_log_message(
            french_message, "en", project_id=project_id
        )
        print(f"\nFrench: {french_message}")
        print(f"English: {english_translation}")
