from __future__ import annotations

import os
from dataclasses import asdict
from typing import Any, AsyncIterable, Dict, Iterable, Optional

from google.cloud import speech_v1p1beta1 as speech
from google.cloud import translate_v3 as translate
from google.cloud import aiplatform_v1beta1 as aiplatform

from speech_models import (
    AudioChunk,
    EmbeddingResult,
    SafetyResult,
    StreamiNgSpeechConfig,
    SummaryResult,
    TranscriptEvent,
    TranslationResult,
    normalize_text,
)


class ConfigError(ValueError):
    pass


class SpeechClientHelper:
    def __init__(self, project_id: Optional[str] = None, location: Optional[str] = None) -> None:
        self.project_id = project_id or os.environ.get("GOOGLE_CLOUD_PROJECT")
        self.location = location or os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")
        if not self.project_id:
            raise ConfigError("GOOGLE_CLOUD_PROJECT is required for Google Cloud integrations")
        self._speech_client = speech.SpeechClient()
        self._translation_client = translate.TranslationServiceClient()
        self._prediction_client = aiplatform.PredictionServiceClient()

    @property
    def parent(self) -> str:
        return f"projects/{self.project_id}/locations/{self.location}"

    def streaming_config(self, language_code: str = "en-US", enable_punctuation: bool = True, model: str = "latest_long") -> speech.StreamingRecognitionConfig:
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=16000,
            language_code=language_code,
            enable_automatic_punctuation=enable_punctuation,
            model=model,
        )
        return speech.StreamingRecognitionConfig(config=config, interim_results=True)

    def recognize_stream(self, audio_chunks: Iterable[bytes], language_code: str = "en-US", enable_punctuation: bool = True, model: str = "latest_long"):
        def requests():
            yield speech.StreamingRecognizeRequest(streaming_config=self.streaming_config(language_code, enable_punctuation, model))
            for chunk in audio_chunks:
                yield speech.StreamingRecognizeRequest(audio_content=chunk)

        return self._speech_client.streaming_recognize(requests=requests())

    async def recognize_async_chunks(self, chunks: AsyncIterable[AudioChunk], language_code: str = "en-US", enable_punctuation: bool = True, model: str = "latest_long"):
        def request_iter():
            yield speech.StreamingRecognizeRequest(streaming_config=self.streaming_config(language_code, enable_punctuation, model))

        for_response = self._speech_client.streaming_recognize(requests=request_iter())
        async for chunk in chunks:
            yield chunk, for_response

    def translate_text(self, text: str, target_language: str) -> TranslationResult:
        request = translate.TranslateTextRequest(
            parent=self.parent,
            contents=[normalize_text(text)],
            mime_type="text/plain",
            target_language_code=target_language,
        )
        response = self._translation_client.translate_text(request=request)
        translated = response.translations[0].translated_text if response.translations else ""
        return TranslationResult(source_text=text, translated_text=translated, target_language=target_language, raw=response.__dict__)

    def moderate_text(self, text: str) -> SafetyResult:
        # Gemini model identifier is intentionally concrete and provider-specific.
        model = "publishers/google/models/gemini-1.5-pro"
        endpoint = f"{self.parent}/{model}"
        instance = {"prompt": normalize_text(text)}
        response = self._prediction_client.predict(endpoint=endpoint, instances=[instance])
        raw = response.__dict__
        unsafe = any(getattr(pred, "content", "") for pred in getattr(response, "predictions", []))
        return SafetyResult(text=text, unsafe=unsafe, categories=["policy" if unsafe else "ok"], raw=raw)

    def summarize_text(self, transcript: str) -> SummaryResult:
        model = "publishers/google/models/gemini-1.5-flash"
        endpoint = f"{self.parent}/{model}"
        instance = {"prompt": f"Summarize the meeting transcript:\n{normalize_text(transcript)}"}
        response = self._prediction_client.predict(endpoint=endpoint, instances=[instance])
        summary = ""
        if getattr(response, "predictions", None):
            summary = str(response.predictions[0])
        return SummaryResult(summary=summary, raw=response.__dict__)

    def embed_text(self, text: str) -> EmbeddingResult:
        model = "publishers/google/models/text-embedding-004"
        endpoint = f"{self.parent}/{model}"
        response = self._prediction_client.predict(endpoint=endpoint, instances=[{"content": normalize_text(text)}])
        embedding = []
        if getattr(response, "predictions", None):
            first = response.predictions[0]
            if isinstance(first, dict):
                embedding = list(first.get("embeddings", first.get("values", [])))
        return EmbeddingResult(text=text, embedding=embedding, raw=response.__dict__)


client = SpeechClientHelper()
