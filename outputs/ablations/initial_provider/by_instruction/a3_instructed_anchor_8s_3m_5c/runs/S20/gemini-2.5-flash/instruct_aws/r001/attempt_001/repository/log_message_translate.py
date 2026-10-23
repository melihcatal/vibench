import os
from google.cloud import translate

def translate_log_message(log_message: str, target_language_code: str = "es") -> dict:
    project_id = os.getenv("GCP_PROJECT_ID")

    if not project_id:
        return {"error": "GCP_PROJECT_ID environment variable not set."}

    client = translate.TranslationServiceClient()

    location = "global"  # For general translation
    parent = f"projects/{project_id}/locations/{location}"

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

        translated_text = " ".join(translations)
        print(f"Successfully translated log message to '{target_language_code}' using Google Cloud Translation API.")
        print(f"Original: {log_message}")
        print(f"Translated: {translated_text}")
        return {"original_message": log_message, "translated_message": translated_text, "target_language": target_language_code}
    except Exception as e:
        print(f"Error translating log message with Google Cloud Translation API: {e}")
        return {"error": f"Failed to translate log message due to an error: {e}"}

# Example Usage (will not be part of the final file)
# if __name__ == "__main__":
#     # os.environ["GCP_PROJECT_ID"] = "your-gcp-project-id"
#     translate_log_message("User login failed due to invalid credentials.", "fr")
#     translate_log_message("Database connection error.") # Defaults to Spanish
