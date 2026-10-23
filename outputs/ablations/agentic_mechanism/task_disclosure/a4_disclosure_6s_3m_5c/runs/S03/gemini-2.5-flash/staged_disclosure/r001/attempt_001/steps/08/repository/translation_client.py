from google.cloud import translate_v2 as translate


class TranslationClient:

  def __init__(self, project_id: str):
    self.client = translate.Client(project=project_id)

  def translate_text(self, text: str, target_language: str) -> str:
    """Translates text into the target language.

    Args:
        text: The text to translate.
        target_language: The language to translate the text to (e.g., "en", "es").

    Returns:
        The translated text.
    """
    response = self.client.translate(
        text,
        target_language=target_language,
        source_language="en",  # Assuming source language is English by default
    )
    return response["translatedText"]
