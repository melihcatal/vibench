import os
from google.cloud import translate_v2 as translate
from observability_models import TranslateRequest

# Ensure GOOGLE_CLOUD_PROJECT environment variable is set
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
if not PROJECT_ID:
    raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

# Initialize Google Cloud Translation client
translate_client = translate.Client(project=PROJECT_ID)


def translate_log_message(request: TranslateRequest) -> str:
    try:
        # The text to translate
        text = request.text
        target_language = request.target_language

        # Target language must be a BCP-47 language code (e.g., "fr" for French)
        if not target_language:
            raise ValueError("Target language must be provided.")

        # Detect source language if not provided (optional, but good practice)
        # detection = translate_client.detect_language(text)
        # source_language = detection['language']
        # print(f"Detected source language: {source_language}")

        result = translate_client.translate(text, target_language=target_language)

        translated_text = result["translatedText"]
        print(f"Original text: '{text}'")
        print(f"Translated text ({target_language}): '{translated_text}'")
        return translated_text

    except Exception as e:
        return f"Error translating log message: {e}"


if __name__ == "__main__":
    # Example usage:
    translate_en_to_es = TranslateRequest(
        text="User logged in successfully from a new device.", target_language="es"
    )
    spanish_translation = translate_log_message(translate_en_to_es)
    print(f"Result: {spanish_translation}")

    print("\n")

    translate_en_to_fr = TranslateRequest(
        text="Failed to connect to the database after 3 retries.", target_language="fr"
    )
    french_translation = translate_log_message(translate_en_to_fr)
    print(f"Result: {french_translation}")
