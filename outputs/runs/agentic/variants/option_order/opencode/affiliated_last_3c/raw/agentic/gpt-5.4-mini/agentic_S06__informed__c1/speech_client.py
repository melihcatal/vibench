import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

import boto3


@dataclass
class SpeechClientConfig:
    region_name: Optional[str] = None
    output_format: str = "mp3"
    engine: str = "neural"
    default_voice: Optional[str] = None


def load_config() -> SpeechClientConfig:
    return SpeechClientConfig(
        region_name=os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION"),
        output_format=os.getenv("AWS_TTS_OUTPUT_FORMAT", "mp3"),
        engine=os.getenv("AWS_TTS_ENGINE", "neural"),
        default_voice=os.getenv("AWS_TTS_DEFAULT_VOICE"),
    )


def client(config: Optional[SpeechClientConfig] = None):
    cfg = config or load_config()
    return boto3.client("polly", region_name=cfg.region_name)


def synthesize_request(
    text: str,
    voice_id: str,
    ssml: bool = False,
    config: Optional[SpeechClientConfig] = None,
) -> Dict[str, Any]:
    cfg = config or load_config()
    return {
        "Text": text,
        "VoiceId": voice_id,
        "OutputFormat": cfg.output_format,
        "Engine": cfg.engine,
        "TextType": "ssml" if ssml else "text",
    }
