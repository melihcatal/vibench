
from google.cloud import translate_v2 as translate

def translate_alt_text(text: str, target_language: str = "en") -> str:
    """
    Translates the given text (image description) to the target language using Google Cloud Translation.

    Args:
        text: The image description to translate.
        target_language: The language to translate the text into (e.g., "en" for English, "es" for Spanish).

    Returns:
        The translated text.
    """
    # Instantiates a client for Google Cloud Translation
    translate_client = translate.Client()

    # The Google Cloud project ID is usually inferred from the environment.
    # If not, you might need to set it explicitly:
    # translate_client = translate.Client(project="your-gcp-project-id")

    response = translate_client.translate(text, target_language=target_language)
    return response["translatedText"]
