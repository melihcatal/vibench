from observability_client import ObservabilityClient
from typing import Dict, Any

def translate_log_message(text: str, target_language: str = "es") -> Dict[str, Any]:
    client = ObservabilityClient()
    translate_client = client.get_translate_client()

    if not translate_client:
        return {"translated_text": text, "detected_source_language": "", "message": "Google Cloud Translation client not configured. Cannot translate.", "success": False}

    try:
        # The translate method can also detect the source language automatically
        result = translate_client.translate(text, target_language=target_language)
        
        translated_text = result["translatedText"]
        detected_source_language = result["detectedSourceLanguage"]

        print(f"Log message translated from {detected_source_language} to {target_language}.")
        return {
            "translated_text": translated_text,
            "detected_source_language": detected_source_language,
            "success": True
        }
    except Exception as e:
        return {"translated_text": text, "detected_source_language": "", "message": f"An error occurred during translation with Google Cloud Translation: {e}", "success": False}

if __name__ == "__main__":
    # Example usage:
    english_message = "User login successful from region us-east-1."
    french_message = "L'utilisateur s'est connecté avec succès depuis la région eu-west-1."
    spanish_message = "El sistema detectó una anomalía en el servidor de base de datos."

    print(f"\nTranslating English message to Spanish: '{english_message}'")
    translated_to_spanish = translate_log_message(english_message, target_language="es")
    print(f"Result: {translated_to_spanish}")

    print(f"\nTranslating French message to English: '{french_message}'")
    translated_to_english = translate_log_message(french_message, target_language="en")
    print(f"Result: {translated_to_english}")

    print(f"\nTranslating Spanish message to German: '{spanish_message}'")
    translated_to_german = translate_log_message(spanish_message, target_language="de")
    print(f"Result: {translated_to_german}")

    # Test with a message that is already in the target language (should still work)
    print(f"\nTranslating Spanish message to Spanish: '{spanish_message}'")
    translated_to_self = translate_log_message(spanish_message, target_language="es")
    print(f"Result: {translated_to_self}")
