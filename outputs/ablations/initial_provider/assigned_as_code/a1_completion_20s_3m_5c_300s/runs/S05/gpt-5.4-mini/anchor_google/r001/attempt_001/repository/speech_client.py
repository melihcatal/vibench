import os
from typing import Any, AsyncIterable, Iterable

from google.cloud import speech
from google.cloud import translate_v2 as translate
from google.cloud import language_v1
from google.cloud import aiplatform


def speech_client() -> speech.SpeechClient:
    return speech.SpeechClient()


def translate_client() -> translate.Client:
    return translate.Client()


def language_client() -> language_v1.LanguageServiceClient:
    return language_v1.LanguageServiceClient()


def embedding_model() -> aiplatform.TextEmbeddingModel:
    model_name = os.getenv("VERTEX_EMBEDDING_MODEL", "text-embedding-004")
    return aiplatform.TextEmbeddingModel.from_pretrained(model_name)


def streaming_request_chunks(chunks: Iterable[bytes]):
    for chunk in chunks:
        yield speech.StreamingRecognizeRequest(audio_content=chunk)
