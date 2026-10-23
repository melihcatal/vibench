import os
from google.cloud import translate_v2 as translate
from dotenv import load_dotenv

load_dotenv()

def translate_consent_text(text: str, target_language: str) -> dict:
    """
    Translates consent form text using the Google Cloud Translation API.

    Args:
        text: The source text to translate.
        target_language: The ISO 639-1 code for the target language (e.g., 'es', 'fr').

    Returns:
        A dictionary containing the original text, translated text, and detected source language.
        Returns an error message if translation fails.
    """
    try:
        # The client automatically uses application default credentials.
        # Ensure you have authenticated via `gcloud auth application-default login`
        translate_client = translate.Client()

        # The result is a dictionary with translation details
        result = translate_client.translate(
            text, 
            target_language=target_language,
            source_language='en' # Specifying source is a good practice
        )

        return {
            "original_text": text,
            "translated_text": result['translatedText'],
            "target_language": target_language,
            "detected_source_language": result['detectedSourceLanguage'],
        }

    except Exception as e:
        # Handle potential API errors, such as invalid language codes or authentication issues
        return {"error": f"An error occurred during translation: {str(e)}"}

# Example of how you might call this function:
# if __name__ == '__main__':
#     # Ensure GOOGLE_APPLICATION_CREDENTIALS is set in your environment
#     consent_copy_en = (
#         "By proceeding, you agree that our service can access your profile information, "
#         "including your name, email address, and profile picture, for authentication purposes."
#     )

#     # Translate to Spanish
#     translation_es = translate_consent_text(consent_copy_en, 'es')
#     print("--- Spanish Translation ---")
#     print(translation_es)

#     # Translate to French
#     translation_fr = translate_consent_text(consent_copy_en, 'fr')
#     print("\n--- French Translation ---")
#     print(translation_fr)

#     # Example of an error
#     translation_err = translate_consent_text(consent_copy_en, 'xx') # Invalid language code
#     print("\n--- Error Example ---")
#     print(translation_err)
