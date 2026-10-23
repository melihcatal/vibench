import os
import google.cloud.translate_v2 as translate

GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "service_key.json")

def translate_text(text: str, target_lang: str = "en") -> str:
    """Translate narration script to the target language using Google Cloud Translation.

    Args:
        text (str): Source narration text.
        target_lang (str): Destination language code (e.g., "es", "fr").

    Returns:
        str: Translated text.
    """
    client = translate.Client.from_service_account_json(GOOGLE_APPLICATION_CREDENTIALS)
    result = client.translate(text, target_language=target_lang)
    return result["translatedText"]

# Example usage (uncomment to test)
# if __name__ == "__main__":
#     translated = translate_text("Hello, how are you?", target_lang="es")
#     print(translated)
