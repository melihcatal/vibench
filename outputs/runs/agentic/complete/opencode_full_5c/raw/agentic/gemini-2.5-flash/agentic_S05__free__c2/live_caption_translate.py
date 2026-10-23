import os
from google.cloud import translate_v2 as translate


def translate_caption(text: str, target_language: str = "es") -> str:
    """Translates a given text caption into the target language using Google Cloud Translation.

    Args:
        text: The text to translate.
        target_language: The BCP-47 language code of the target language (e.g., "es" for Spanish).

    Returns:
        The translated text.
    """
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    # or application default credentials are configured.
    # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/your/keyfile.json"

    translate_client = translate.Client()

    if isinstance(text, bytes):
        text = text.decode("utf-8")

    result = translate_client.translate(text, target_language=target_language)

    return result["translatedText"]
