from google.cloud import translate_v2 as translate
from speech_models import TranscriptResult

class LiveCaptionTranslator:
    def __init__(self, target_language: str = "es"):
        self.translate_client = translate.Client()
        self.target_language = target_language

    def translate_caption(self, caption: TranscriptResult) -> str:
        if not caption.text.strip():
            return ""

        # Google Cloud Translation API expects a list of texts
        result = self.translate_client.translate(caption.text, target_language=self.target_language)
        translated_text = result["translatedText"]
        print(f"Original: {caption.text} -> Translated ({self.target_language}): {translated_text}")
        return translated_text

if __name__ == "__main__":
    # Example usage
    translator = LiveCaptionTranslator(target_language="fr")
    sample_caption = TranscriptResult(text="Hello world, how are you?", is_partial=False, language="en-US")
    translated_caption = translator.translate_caption(sample_caption)
    print(f"Translated caption: {translated_caption}")
