from google.cloud import translate_v2 as translate
from google.api_core.exceptions import GoogleAPICallError

def translate_log_message(text: str, target_language: str) -> str:
    """
    Translates a log message to a specified language using Google Cloud Translate.

    Args:
        text: The log message to translate.
        target_language: The ISO 639-1 code for the target language (e.g., 'es', 'fr').

    Returns:
        The translated message, or an error string.
    """
    try:
        # This client uses Application Default Credentials to authenticate.
        # Ensure you have run `gcloud auth application-default login`
        translate_client = translate.Client()
    except Exception as e:
        return f"Failed to initialize Google Translate client: {e}"

    if not isinstance(text, str) or not text:
        return "Input text must be a non-empty string."

    try:
        result = translate_client.translate(text, target_language=target_language)
        return result['translatedText']
    except GoogleAPICallError as e:
        return f"Error during translation API call: {e}"
    except Exception as e:
        return f"An unexpected error occurred: {e}"


if __name__ == "__main__":
    # This log message might be shown to a Spanish-speaking support agent.
    original_message = "User 'usr-54321' failed to update payment method due to insufficient funds."
    target_locale = "es"

    print(f"Original message (en): {original_message}")
    
    translated_message = translate_log_message(original_message, target_locale)
    
    print(f"Translated message ({target_locale}): {translated_message}")

    # Example of an error
    invalid_message = translate_log_message(original_message, "xx") # invalid language code
    print(f"\nAttempting translation with invalid code 'xx': {invalid_message}")
