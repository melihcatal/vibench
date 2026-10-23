from google.cloud import translate_v2 as translate

class LiveCaptionTranslator:
    def __init__(self, project_id: str):
        self.client = translate.Client(project=project_id)

    def translate_text(self, text: str, target_language: str, source_language: str = "en") -> str:
        """
        Translates text into the target language.

        Args:
            text: The text to translate.
            target_language: The language to translate the text into (e.g., "es" for Spanish).
            source_language: The language of the input text (e.g., "en" for English).

        Returns:
            The translated text.
        """
        if isinstance(text, bytes):
            text = text.decode("utf-8")

        result = self.client.translate(
            text, target_language=target_language, source_language=source_language
        )

        return result["translatedText"]

