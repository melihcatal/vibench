import json
import os
from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional

from google.cloud import speech_v1p1beta1 as speech


@dataclass
class RecognitionResult:
    text: str
    is_final: bool
    confidence: Optional[float] = None


def _build_client() -> speech.SpeechClient:
    return speech.SpeechClient()


def _streaming_config() -> speech.StreamingRecognitionConfig:
    return speech.StreamingRecognitionConfig(
        config=speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=int(os.getenv("GOOGLE_SPEECH_SAMPLE_RATE", "16000")),
            language_code=os.getenv("GOOGLE_SPEECH_LANGUAGE", "en-US"),
            enable_automatic_punctuation=True,
        ),
        interim_results=True,
        single_utterance=False,
    )


def handle_streaming_recognition(audio_chunks: List[bytes], on_result: Callable[[RecognitionResult], None]) -> List[RecognitionResult]:
    client = _build_client()
    config = _streaming_config()

    def requests() -> Any:
        yield speech.StreamingRecognizeRequest(streaming_config=config)
        for chunk in audio_chunks:
            yield speech.StreamingRecognizeRequest(audio_content=chunk)

    results: List[RecognitionResult] = []
    for response in client.streaming_recognize(requests())
        :
        for result in response.results:
            if not result.alternatives:
                continue
            transcript = result.alternatives[0].transcript.strip()
            if not transcript:
                continue
            partial = RecognitionResult(
                text=transcript,
                is_final=result.is_final,
                confidence=getattr(result.alternatives[0], "confidence", None),
            )
            results.append(partial)
            on_result(partial)

    return results


def parse_recognition_event(payload: Dict[str, Any]) -> RecognitionResult:
    text = payload.get("transcript") or payload.get("text") or ""
    is_final = bool(payload.get("is_final", payload.get("final", False)))
    confidence = payload.get("confidence")
    return RecognitionResult(text=text, is_final=is_final, confidence=confidence)


def merge_results(results: List[RecognitionResult]) -> str:
    committed: List[str] = []
    partial: str = ""
    for item in results:
        if item.is_final:
            if item.text:
                committed.append(item.text)
            partial = ""
        else:
            partial = item.text
    if partial:
        committed.append(partial)
    return " ".join(committed).strip()
