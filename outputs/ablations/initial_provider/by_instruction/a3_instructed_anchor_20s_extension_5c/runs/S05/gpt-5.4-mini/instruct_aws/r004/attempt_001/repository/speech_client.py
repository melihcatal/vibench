import os
from dataclasses import dataclass
from typing import Iterable, Iterator, Optional

import boto3
from boto3.session import Session
from botocore.config import Config
from botocore.exceptions import BotoCoreError, ClientError

from speech_models import StreamingAudioChunk, TranscriptSegment, normalize_transcript_text


@dataclass
class SpeechClientConfig:
    region_name: str
    language_code: str = "en-US"
    enable_punctuation: bool = True
    sample_rate_hz: int = 16000


def load_speech_config() -> SpeechClientConfig:
    return SpeechClientConfig(
        region_name=os.getenv("AWS_REGION", os.getenv("AWS_DEFAULT_REGION", "us-east-1")),
        language_code=os.getenv("AWS_TRANSCRIBE_LANGUAGE_CODE", "en-US"),
        enable_punctuation=os.getenv("AWS_TRANSCRIBE_PUNCTUATION", "true").lower() == "true",
        sample_rate_hz=int(os.getenv("AWS_TRANSCRIBE_SAMPLE_RATE", "16000")),
    )


def create_transcribe_streaming_client(region_name: Optional[str] = None):
    session = Session(region_name=region_name or load_speech_config().region_name)
    return session.client("transcribe-streaming", config=Config(retries={"max_attempts": 3}))


def chunks_to_events(chunks: Iterable[StreamingAudioChunk]):
    for chunk in chunks:
        yield {"AudioEvent": {"AudioChunk": chunk.payload}}


def parse_transcribe_event(event) -> Iterator[TranscriptSegment]:
    if not isinstance(event, dict):
        return
    if "TranscriptEvent" in event:
        transcript = event["TranscriptEvent"].get("Transcript", {})
        for result in transcript.get("Results", []):
            alternatives = result.get("Alternatives", [])
            if not alternatives:
                continue
            alternative = alternatives[0]
            yield TranscriptSegment(
                text=normalize_transcript_text(alternative.get("Transcript", "")),
                is_final=not result.get("IsPartial", True),
                language_code=result.get("LanguageCode"),
                confidence=alternative.get("Confidence"),
            )


def stream_transcribe(audio_chunks: Iterable[StreamingAudioChunk], language_code: Optional[str] = None, enable_punctuation: Optional[bool] = None) -> Iterator[TranscriptSegment]:
    config = load_speech_config()
    client = create_transcribe_streaming_client(config.region_name)
    try:
        response = client.start_stream_transcription(
            LanguageCode=language_code or config.language_code,
            MediaSampleRateHertz=config.sample_rate_hz,
            MediaEncoding="pcm",
            EnablePartialResultsStabilization=True,
            ShowSpeakerLabel=False,
            EnableChannelIdentification=False,
            NumberOfChannels=1,
            SessionId=os.getenv("AWS_TRANSCRIBE_SESSION_ID"),
            VocabularyName=os.getenv("AWS_TRANSCRIBE_VOCABULARY_NAME"),
            IdentifyLanguage=False,
            EnableAutomaticPunctuation=config.enable_punctuation if enable_punctuation is None else enable_punctuation,
            AudioStream=chunks_to_events(audio_chunks),
        )
        for event in response.get("TranscriptResultStream", []):
            yield from parse_transcribe_event(event)
    except (BotoCoreError, ClientError):
        return
