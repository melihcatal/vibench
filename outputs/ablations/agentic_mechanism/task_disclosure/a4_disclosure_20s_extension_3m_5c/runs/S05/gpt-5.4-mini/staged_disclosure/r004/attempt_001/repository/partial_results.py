import os
import json
import base64
from typing import Any, Dict, Iterable, List, Optional

from google.cloud import speech_v1p1beta1 as speech


def _recognizer_client() -> speech.SpeechClient:
    return speech.SpeechClient()


def _streaming_config(language_code: str = "en-US") -> speech.StreamingRecognitionConfig:
    recognition_config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code=language_code,
        enable_automatic_punctuation=True,
        model="latest_long",
    )
    return speech.StreamingRecognitionConfig(
        config=recognition_config,
        interim_results=True,
        single_utterance=False,
    )


def _audio_requests(chunks: Iterable[bytes]) -> Iterable[speech.StreamingRecognizeRequest]:
    for chunk in chunks:
        if chunk:
            yield speech.StreamingRecognizeRequest(audio_content=chunk)


def handle_streaming_recognition(chunks: Iterable[bytes], language_code: str = "en-US") -> List[Dict[str, Any]]:
    client = _recognizer_client()
    config = _streaming_config(language_code=language_code)
    requests = _audio_requests(chunks)
    responses = client.streaming_recognize(config=config, requests=requests)
    events: List[Dict[str, Any]] = []
    for response in responses:
        if not response.results:
            continue
        for result in response.results:
            if not result.alternatives:
                continue
            transcript = result.alternatives[0].transcript
            events.append(
                {
                    "transcript": transcript,
                    "is_final": bool(result.is_final),
                    "stability": getattr(result, "stability", None),
                }
            )
    return events


def parse_base64_audio_chunks(payload: str) -> List[bytes]:
    data = json.loads(payload)
    chunks = data.get("chunks", [])
    return [base64.b64decode(chunk) for chunk in chunks]


def process_payload(payload: str, language_code: str = "en-US") -> List[Dict[str, Any]]:
    return handle_streaming_recognition(parse_base64_audio_chunks(payload), language_code=language_code)
