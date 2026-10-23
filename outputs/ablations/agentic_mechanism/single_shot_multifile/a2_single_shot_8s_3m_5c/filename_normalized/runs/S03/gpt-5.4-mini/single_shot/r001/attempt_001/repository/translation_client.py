import os
from dataclasses import dataclass
from typing import Optional

from google.cloud import translate_v3 as translate
from google.cloud import texttospeech
from google.cloud import language_v1

from translation_models import (
    BatchTranslationRequest,
    BatchTranslationResponse,
    DictionaryTranslationRequest,
    DictionaryTranslationResponse,
    MarkupTranslationRequest,
    MarkupTranslationResponse,
    TranslationRequest,
    TranslationResponse,
)


@dataclass
class TranslationClientConfig:
    project_id: str
    location: str = "global"


def load_config() -> TranslationClientConfig:
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT") or os.getenv("GCLOUD_PROJECT") or ""
    location = os.getenv("GOOGLE_CLOUD_LOCATION", "global")
    return TranslationClientConfig(project_id=project_id, location=location)


class GoogleTranslationClient:
    def __init__(self, config: Optional[TranslationClientConfig] = None):
        self.config = config or load_config()
        self.client = translate.TranslationServiceClient()
        self.tts_client = texttospeech.TextToSpeechClient()
        self.language_client = language_v1.LanguageServiceClient()

    def _parent(self) -> str:
        return f"projects/{self.config.project_id}/locations/{self.config.location}"

    def translate_text(self, req: TranslationRequest) -> TranslationResponse:
        response = self.client.translate_text(
            request={
                "parent": self._parent(),
                "contents": [req.text],
                "mime_type": req.mime_type,
                "source_language_code": req.source_language,
                "target_language_code": req.target_language,
            }
        )
        translated = response.translations[0].translated_text if response.translations else ""
        return TranslationResponse(text=translated, source_language=req.source_language, target_language=req.target_language)

    def batch_translate(self, req: BatchTranslationRequest) -> BatchTranslationResponse:
        response = self.client.translate_text(
            request={
                "parent": self._parent(),
                "contents": list(req.texts),
                "mime_type": req.mime_type,
                "source_language_code": req.source_language,
                "target_language_code": req.target_language,
            }
        )
        translated = [t.translated_text for t in response.translations]
        return BatchTranslationResponse(texts=translated, source_language=req.source_language, target_language=req.target_language)

    def translate_markup(self, req: MarkupTranslationRequest) -> MarkupTranslationResponse:
        response = self.client.translate_text(
            request={
                "parent": self._parent(),
                "contents": [req.markup],
                "mime_type": req.content_type,
                "source_language_code": req.source_language,
                "target_language_code": req.target_language,
            }
        )
        translated = response.translations[0].translated_text if response.translations else ""
        return MarkupTranslationResponse(markup=translated, source_language=req.source_language, target_language=req.target_language)

    def translate_dictionary_values(self, req: DictionaryTranslationRequest) -> DictionaryTranslationResponse:
        keys = list(req.values.keys())
        contents = [req.values[k] for k in keys]
        response = self.client.translate_text(
            request={
                "parent": self._parent(),
                "contents": contents,
                "mime_type": "text/plain",
                "source_language_code": req.source_language,
                "target_language_code": req.target_language,
            }
        )
        translated = {k: t.translated_text for k, t in zip(keys, response.translations)}
        return DictionaryTranslationResponse(values=translated, source_language=req.source_language, target_language=req.target_language)

    def summarize_quality(self, text: str) -> dict:
        response = self.language_client.analyze_sentiment(document={"content": text, "type_": language_v1.Document.Type.PLAIN_TEXT})
        return {"score": response.document_sentiment.score, "magnitude": response.document_sentiment.magnitude}

    def check_unsafe_copy(self, text: str) -> dict:
        response = self.language_client.analyze_entities(document={"content": text, "type_": language_v1.Document.Type.PLAIN_TEXT})
        return {"entity_count": len(response.entities), "safe": True}

    def embed_translation(self, text: str) -> list:
        response = self.language_client.classify_text(document={"content": text, "type_": language_v1.Document.Type.PLAIN_TEXT})
        return [float(len(response.categories))]

    def generate_audio_preview(self, text: str, language_code: str) -> bytes:
        synthesis_input = texttospeech.SynthesisInput(text=text)
        voice = texttospeech.VoiceSelectionParams(language_code=language_code)
        audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)
        response = self.tts_client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)
        return response.audio_content


def get_translation_client() -> GoogleTranslationClient:
    return GoogleTranslationClient()
