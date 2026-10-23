import os
from google.cloud import translate_v2 as translate
from typing import List, Dict, Any

def translate_log_message(text: str, target_language: str = "es", source_language: str = None) -> Dict[str, Any]:
    """Translates a support-visible log message for another locale using Google Cloud Translation."""
    # Google Cloud Translation client automatically picks up GOOGLE_APPLICATION_CREDENTIALS
    # or other default credentials.
    translate_client = translate.Client()

    if isinstance(text, bytes):
        text = text.decode("utf-8")

    try:
        # API documentation: https://cloud.google.com/translate/docs/reference/rest/v2/translate
        result = translate_client.translate(text,
                                            target_language=target_language,
                                            source_language=source_language)
        
        return {
            "original_text": text,
            "translated_text": result['translatedText'],
            "source_language": result['detectedSourceLanguage'],
            "target_language": target_language
        }
    except Exception as e:
        return {"error": str(e), "original_text": text}

def translate_log_messages_batch(messages: List[str], target_language: str = "es") -> List[Dict[str, Any]]:
    """Translates a batch of log messages."""
    # The translate_client.translate method can handle a single string or a list of strings.
    # However, for simplicity and explicit mapping, processing one by one for now.
    # For real batching, consider using client.translate with multiple texts.
    translated_results = []
    for msg in messages:
        translated_results.append(translate_log_message(msg, target_language))
    return translated_results

if __name__ == "__main__":
    # Example usage:
    # Set GOOGLE_APPLICATION_CREDENTIALS environment variable or configure default credentials
    # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/your/keyfile.json"

    log_message1 = "User 'johndoe' failed to authenticate due to invalid credentials."
    log_message2 = "Database connection error: Connection refused."
    log_message3 = "New product feature 'X' released successfully."

    print(f"\nTranslating: '{log_message1}' to Spanish")
    translated_msg1 = translate_log_message(log_message1, target_language="es")
    print(translated_msg1)

    print(f"\nTranslating: '{log_message2}' to German")
    translated_msg2 = translate_log_message(log_message2, target_language="de")
    print(translated_msg2)

    print(f"\nTranslating batch of messages to French")
    messages_to_batch_translate = [
        log_message1,
        log_message2,
        log_message3
    ]
    translated_batch = translate_log_messages_batch(messages_to_batch_translate, target_language="fr")
    for result in translated_batch:
        print(result)
