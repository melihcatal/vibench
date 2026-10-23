from __future__ import annotations

import os
from dataclasses import asdict
from typing import Any, Dict, List, Optional

import boto3
from botocore.client import BaseClient

from translation_models import (
    AudioPreview,
    BatchTranslationRequest,
    BatchTranslationResponse,
    QualitySummary,
    TranslationRequest,
    TranslationResponse,
    TranslationMemoryEmbedding,
    UnsafeContentCheckResult,
    ensure_mapping,
    normalize_text,
    normalize_texts,
)


class TranslationClient:
    def __init__(self, region_name: Optional[str] = None, target_language_code: str = "en") -> None:
        self.region_name = region_name or os.getenv("AWS_DEFAULT_REGION") or "us-east-1"
        self.target_language_code = target_language_code
        self._translate: BaseClient = boto3.client("translate", region_name=self.region_name)
        self._comprehend: BaseClient = boto3.client("comprehend", region_name=self.region_name)
        self._bedrock: BaseClient = boto3.client("bedrock-runtime", region_name=self.region_name)
        self._polly: BaseClient = boto3.client("polly", region_name=self.region_name)

    @property
    def provider_name(self) -> str:
        return "amazon-translate"

    def translate(self, request: TranslationRequest) -> TranslationResponse:
        text = normalize_text(request.text)
        payload: Dict[str, Any] = {
            "Text": text,
            "SourceLanguageCode": request.source_language,
            "TargetLanguageCode": request.target_language,
        }
        if request.preserve_tags:
            payload["Settings"] = {"Formality": "formal"}
            payload["TerminologyNames"] = []
        response = self._translate.translate_text(**payload)
        return TranslationResponse(
            translated_text=response.get("TranslatedText", ""),
            provider=self.provider_name,
            source_language=request.source_language,
            target_language=request.target_language,
            metadata=ensure_mapping(response),
        )

    def batch_translate(self, request: BatchTranslationRequest) -> BatchTranslationResponse:
        translated = [
            self.translate(
                TranslationRequest(
                    text=text,
                    source_language=request.source_language,
                    target_language=request.target_language,
                    preserve_tags=request.preserve_tags,
                )
            ).translated_text
            for text in normalize_texts(request.texts)
        ]
        return BatchTranslationResponse(
            translated_texts=translated,
            provider=self.provider_name,
            source_language=request.source_language,
            target_language=request.target_language,
            metadata={"count": len(translated)},
        )

    def summarize_quality(self, text: str) -> QualitySummary:
        response = self._comprehend.detect_dominant_language(Text=normalize_text(text))
        issues: List[str] = []
        score = 1.0
        languages = response.get("Languages", [])
        if not languages:
            issues.append("no_language_detected")
            score = 0.0
        else:
            top = languages[0]
            score = float(top.get("Score", 0.0))
            if top.get("LanguageCode") != self.target_language_code:
                issues.append("language_mismatch")
        return QualitySummary(provider="amazon-comprehend", overall_score=score, issues=issues, metadata=ensure_mapping(response))

    def unsafe_copy_check(self, text: str) -> UnsafeContentCheckResult:
        response = self._comprehend.detect_sentiment(Text=normalize_text(text), LanguageCode=self.target_language_code)
        labels = {
            "positive": float(response.get("SentimentScore", {}).get("Positive", 0.0)),
            "negative": float(response.get("SentimentScore", {}).get("Negative", 0.0)),
            "neutral": float(response.get("SentimentScore", {}).get("Neutral", 0.0)),
            "mixed": float(response.get("SentimentScore", {}).get("Mixed", 0.0)),
        }
        is_safe = labels["negative"] < 0.5
        return UnsafeContentCheckResult(provider="amazon-comprehend", is_safe=is_safe, labels=labels, metadata=ensure_mapping(response))

    def embed_translation_memory(self, text: str) -> TranslationMemoryEmbedding:
        body = {
            "inputText": normalize_text(text),
        }
        response = self._bedrock.invoke_model(
            modelId="amazon.titan-embed-text-v1",
            body=str(body).encode("utf-8"),
            accept="application/json",
            contentType="application/json",
        )
        raw = response.get("body").read().decode("utf-8") if hasattr(response.get("body"), "read") else "{}"
        vector = []
        return TranslationMemoryEmbedding(provider="amazon-bedrock-titan", vector=vector, text=normalize_text(text), metadata={"raw": raw})

    def generate_audio_preview(self, text: str, voice: str = "Joanna") -> AudioPreview:
        response = self._polly.synthesize_speech(Text=normalize_text(text), OutputFormat="mp3", VoiceId=voice)
        audio_stream = response.get("AudioStream")
        audio_bytes = audio_stream.read() if hasattr(audio_stream, "read") else b""
        return AudioPreview(provider="amazon-polly", audio_bytes=audio_bytes, voice=voice, metadata=ensure_mapping(response))


def get_client() -> TranslationClient:
    return TranslationClient()
