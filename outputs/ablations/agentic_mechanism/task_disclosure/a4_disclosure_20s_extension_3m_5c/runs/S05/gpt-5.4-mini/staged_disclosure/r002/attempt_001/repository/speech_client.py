import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

import boto3


@dataclass
class SpeechClientConfig:
    region_name: str = os.getenv("AWS_REGION", os.getenv("AWS_DEFAULT_REGION", "us-east-1"))
    language_code: str = os.getenv("TRANSCRIPTION_LANGUAGE", "en-US")
    sample_rate_hz: int = int(os.getenv("AUDIO_SAMPLE_RATE", "16000"))
    media_encoding: str = os.getenv("AUDIO_ENCODING", "pcm")
    vocabulary_name: Optional[str] = os.getenv("AWS_TRANSCRIBE_VOCABULARY")
    show_speaker_labels: bool = os.getenv("AWS_TRANSCRIBE_SPEAKER_LABELS", "false").lower() == "true"
    enable_partial_results_stabilization: bool = os.getenv("AWS_TRANSCRIBE_PARTIAL_RESULTS_STABILIZATION", "true").lower() == "true"
    partial_results_stability: str = os.getenv("AWS_TRANSCRIBE_PARTIAL_RESULTS_STABILITY", "high")


def load_speech_config() -> SpeechClientConfig:
    return SpeechClientConfig()


def create_transcribe_client(config: Optional[SpeechClientConfig] = None):
    cfg = config or load_speech_config()
    return boto3.client("transcribe", region_name=cfg.region_name)


def create_streaming_transcription_request(config: Optional[SpeechClientConfig] = None) -> Dict[str, Any]:
    cfg = config or load_speech_config()
    request: Dict[str, Any] = {
        "LanguageCode": cfg.language_code,
        "MediaSampleRateHertz": cfg.sample_rate_hz,
        "MediaEncoding": cfg.media_encoding,
        "EnablePartialResultsStabilization": cfg.enable_partial_results_stabilization,
        "PartialResultsStability": cfg.partial_results_stability,
    }
    if cfg.vocabulary_name:
        request["VocabularyName"] = cfg.vocabulary_name
    if cfg.show_speaker_labels:
        request["ShowSpeakerLabels"] = True
    return request


def start_streaming_transcription(client: Any, audio_stream: Any, config: Optional[SpeechClientConfig] = None) -> Any:
    request = create_streaming_transcription_request(config)
    return client.start_stream_transcription(AudioStream=audio_stream, **request)
