from google.cloud import translate_v2 as translate
from speech_models import SpeechRecognitionResult
from typing import Iterator

class Translator:
    def __init__(self, target_language: str):
        self._client = translate.Client()
        self.target_language = target_language

    def translate_caption(self, caption: SpeechRecognitionResult) -> SpeechRecognitionResult:
        if not caption.text:
            return caption

        # Google Cloud Translation API
        # The source language is automatically detected by the API if not specified.
        translation = self._client.translate(
            caption.text, target_language=self.target_language)

        return SpeechRecognitionResult(
            text=translation["translatedText"],
            is_final=caption.is_final,
            language_code=self.target_language # Update to the target language
        )

def live_caption_translate(captions: Iterator[SpeechRecognitionResult], target_language: str) -> Iterator[SpeechRecognitionResult]:
    translator = Translator(target_language)
    for caption in captions:
        yield translator.translate_caption(caption)
