
import os
from google.cloud import translate_v2 as translate

def translate_text(text: str, target_language: str) -> str:
    """Translates text into the target language.

    Args:
        text: The text to translate.
        target_language: The language to translate the text into (e.g., "es" for Spanish).

    Returns:
        The translated text.
    """
    # Google Cloud Translation API expects the GOOGLE_APPLICATION_CREDENTIALS
    # environment variable to be set to the path of a service account key file.
    # For more information, see:
    # https://cloud.google.com/docs/authentication/getting-started
    translate_client = translate.Client()

    result = translate_client.translate(
        text,
        target_language=target_language
    )

    return result['''translatedText''']

if __name__ == "__main__":
    # Example usage:
    # Set the GOOGLE_APPLICATION_CREDENTIALS environment variable
    # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/your/keyfile.json"

    # translated_output = translate_text("Hello, world!", "es")
    # print(f"Translated text: {translated_output}")
    pass
