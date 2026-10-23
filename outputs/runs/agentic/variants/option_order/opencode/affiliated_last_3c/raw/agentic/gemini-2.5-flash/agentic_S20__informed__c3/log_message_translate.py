import os
from google.cloud import translate


def translate_log_message(
    log_message: str, target_language_code: str = "es", project_id: Optional[str] = None
) -> dict:
    # GOOGLE_APPLICATION_CREDENTIALS environment variable should be set
    # or explicitly pass project_id
    if not project_id:
        project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        return {
            "error": "Google Cloud Project ID not provided and GOOGLE_CLOUD_PROJECT env var not set."
        }

    client = translate.TranslationServiceClient()

    parent = f"projects/{project_id}"

    try:
        response = client.translate_text(
            request={
                "parent": parent,
                "contents": [log_message],
                "target_language_code": target_language_code,
            }
        )

        translations = []
        for translation in response.translations:
            translations.append(translation.translated_text)

        return {
            "original_message": log_message,
            "target_language": target_language_code,
            "translated_messages": translations,
        }

    except Exception as e:
        return {
            "error": f"Error translating log message with Google Cloud Translation: {e}"
        }


if __name__ == "__main__":
    # Example usage
    message_en = "User 'johndoe' failed to authenticate due to incorrect password."
    message_fr = (
        "L'utilisateur 'janedoe' a rencontré une erreur lors de l'accès à la ressource."
    )

    # Replace with your actual Google Cloud Project ID
    # os.environ["GOOGLE_CLOUD_PROJECT"] = "your-gcp-project-id"
    # For demonstration, we'll assume GOOGLE_CLOUD_PROJECT is set or pass None and let it fail if not set.

    translated_to_spanish = translate_log_message(message_en, target_language_code="es")
    translated_to_french = translate_log_message(message_en, target_language_code="fr")
    translated_to_german = translate_log_message(message_fr, target_language_code="de")

    print("\n--- English to Spanish ---")
    print(translated_to_spanish)

    print("\n--- English to French ---")
    print(translated_to_french)

    print("\n--- French to German ---")
    print(translated_to_german)
