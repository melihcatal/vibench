from __future__ import annotations

from typing import Any, Dict

import boto3

from model_client import load_config



def platform_brief_audio(text: str) -> Dict[str, Any]:
    config = load_config()
    client = boto3.client("polly", region_name=config.aws_region)
    result = client.synthesize_speech(Text=text, OutputFormat="mp3", VoiceId=config.tts_voice_id)
    return {
        "provider": "Amazon Polly",
        "voice_id": config.tts_voice_id,
        "audio_stream": result["AudioStream"],
        "content_type": result.get("ContentType", "audio/mpeg"),
    }
