import os
from google.cloud import translate

def translate_log_message(text: str, target_language: str = "es", project_id: str = None) -> str:
    """Translates support-visible log messages for another locale using Google Cloud Translation."""
    if not project_id:
        project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        return "Error: GCP project ID not provided and GOOGLE_CLOUD_PROJECT environment variable not set."

    client = translate.TranslationServiceClient()

    parent = f"projects/{project_id}/locations/global"

    try:
        response = client.translate_text(
            request={
                "parent": parent,
                "contents": [text],
                "target_language_code": target_language,
            }
        )

        if response.translations:
            translated_text = response.translations[0].translated_text
            print(f"Translated message from \'{text}\' to \'{target_language}\' as \'{translated_text}\'")
            return translated_text
        else:
            return f"No translation found for '{text}'"
    except Exception as e:
        return f"Error calling Google Cloud Translation API: {e}"

if __name__ == "__main__":
    # Example usage:
    # Ensure GOOGLE_APPLICATION_CREDENTIALS and GOOGLE_CLOUD_PROJECT environment variables are set
    gcp_project_id = os.getenv("GOOGLE_CLOUD_PROJECT", "your-gcp-project-id")
    if gcp_project_id == "your-gcp-project-id":
        print("Please set GOOGLE_CLOUD_PROJECT environment variable or replace 'your-gcp-project-id' in the script.")
    else:
        english_log = "Failed to connect to external service. Retrying..."
        spanish_log = translate_log_message(english_log, target_language="es", project_id=gcp_project_id)
        print(f"Original: {english_log}")
        print(f"Spanish: {spanish_log}")

        german_log = translate_log_message("User session expired.", target_language="de", project_id=gcp_project_id)
        print(f"Original: User session expired.")
        print(f"German: {german_log}")
