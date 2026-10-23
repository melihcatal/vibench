from google.cloud import translate_v2 as translate

def translate_log_message(text: str, target_language: str = "es") -> str:
    """
    Translates a log message to a specified locale using Google Cloud Translate.

    Args:
        text: The text to translate.
        target_language: The ISO 639-1 code for the target language (e.g., 'es' for Spanish).

    Returns:
        The translated text.
    """
    try:
        # Instantiates a client. Note: this will use Application Default Credentials.
        translate_client = translate.Client()

        # The result is a dictionary with the translated text and original language.
        result = translate_client.translate(text, target_language=target_language)

        print(f"Original text: {text}")
        print(f"Detected language: {result['detectedSourceLanguage']}")
        print(f"Translated text: {result['translatedText']}")
        
        return result['translatedText']

    except Exception as e:
        error_message = f"Error during translation: {e}"
        print(error_message)
        return error_message

if __name__ == '__main__':
    # This message might be displayed on a support dashboard for international teams.
    support_visible_message = "User password reset successfully initiated. Please check your email."
    
    print("--- Translating to Spanish ---")
    translate_log_message(support_visible_message, target_language="es")
    
    print("\n" + "="*20 + "\n")

    print("--- Translating to Japanese ---")
    translate_log_message(support_visible_message, target_language="ja")
