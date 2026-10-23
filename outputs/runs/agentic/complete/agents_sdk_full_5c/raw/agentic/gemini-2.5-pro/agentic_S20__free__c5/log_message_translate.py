import os
from google.cloud import translate_v2 as translate

def translate_log_message(text: str, target_language: str = "es"):
    """
    Translates a log message text to a specified language using
    the Google Cloud Translate API.

    Args:
        text: The log message to translate.
        target_language: The ISO 639-1 code for the target language (e.g., 'es' for Spanish).
    
    Returns:
        The translated text, or None if an error occurs.
    """
    try:
        # This client uses the Application Default Credentials strategy
        # for authentication, expecting GOOGLE_APPLICATION_CREDENTIALS.
        translate_client = translate.Client()

        print(f"Original message (en): '{text}'")

        # The result is a dictionary that includes the translated text.
        result = translate_client.translate(text, target_language=target_language)
        
        translated_text = result['translatedText']
        detected_language = result['detectedSourceLanguage']
        
        print(f"Detected source language: {detected_language}")
        print(f"Translated message ({target_language}): '{translated_text}'")
        
        return translated_text

    except Exception as e:
        print(f"An error occurred during translation: {e}")
        return None

if __name__ == '__main__':
    # This message is intended for an international support team.
    support_visible_log = "User authentication failed due to an invalid password. Please advise the user to reset their password."
    translate_log_message(support_visible_log, "es") # Spanish
    print("-" * 20)
    translate_log_message(support_visible_log, "fr") # French
    print("-" * 20)
    translate_log_message(support_visible_log, "ja") # Japanese
