import os
from dataclasses import dataclass
from typing import AsyncIterable, AsyncIterator, Iterable, List, Optional

from google.cloud import speech_v1p1beta1 as speech

from speech_models import AudioChunk, StreamingTranscriptionRequest, TranscriptSegment, normalize_transcript


@dataclass
class SpeechConfig:
    project_id: Optional[str] = None
    location: Optional[str] = None
    language_code: str = "en-US"
    enable_punctuation: bool = True
    model: str = "latest_long"


def load_speech_config() -> SpeechConfig:
    return SpeechConfig(
        project_id=os.getenv("GOOGLE_CLOUD_PROJECT"),
        location=os.getenv("GOOGLE_CLOUD_LOCATION"),
        language_code=os.getenv("GOOGLE_SPEECH_LANGUAGE_CODE", "en-US"),
        enable_punctuation=os.getenv("GOOGLE_SPEECH_ENABLE_PUNCTUATION", "true").lower() == "true",
        model=os.getenv("GOOGLE_SPEECH_MODEL", "latest_long"),
    )


def make_client() -> speech.SpeechClient:
    return speech.SpeechClient()


def build_streaming_config(cfg: SpeechConfig) -> speech.StreamingRecognitionConfig:
    recognition_config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code=cfg.language_code,
        enable_automatic_punctuation=cfg.enable_punctuation,
        model=cfg.model,
    )
    return speech.StreamingRecognitionConfig(config=recognition_config, interim_results=True, single_utterance=False)


def chunk_to_request(chunk: AudioChunk) -> speech.StreamingRecognizeRequest:
    return speech.StreamingRecognizeRequest(audio_content=chunk.data)


def transcript_segments_from_response(response: speech.StreamingRecognizeResponse) -> List[TranscriptSegment]:
    segments: List[TranscriptSegment] = []
    for result in response.results:
        if not result.alternatives:
            continue
        alt = result.alternatives[0]
        segments.append(
            TranscriptSegment(
                text=normalize_transcript(alt.transcript),
                is_final=result.is_final,
                confidence=getattr(alt, "confidence", None),
                language_code=getattr(response, "language_code", None),
            )
        )
    return segments


async def stream_recognize(source: AsyncIterable[bytes], cfg: Optional[SpeechConfig] = None) -> AsyncIterator[TranscriptSegment]:
    config = cfg or load_speech_config()
    client = make_client()
    requests = [speech.StreamingRecognizeRequest(streaming_config=build_streaming_config(config))]
    async for item in source:
        requests.append(speech.StreamingRecognizeRequest(audio_content=item))
    for response in client.streaming_recognize(requests=requests):
        for segment in transcript_segments_from_response(response):
            yield segment
