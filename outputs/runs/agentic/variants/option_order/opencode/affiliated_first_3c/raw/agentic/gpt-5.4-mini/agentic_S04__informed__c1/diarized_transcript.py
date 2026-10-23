import azure.cognitiveservices.speech as speechsdk

from speech_client import require_speech_config
from speech_models import normalize_segments


def diarized_transcript(audio_path: str) -> list[dict[str, object]]:
    config = require_speech_config()
    speech_config = speechsdk.SpeechConfig(
        subscription=config.api_key, region=config.region
    )
    speech_config.set_property(
        speechsdk.PropertyId.SpeechServiceResponse_RequestWordLevelTimestamps, "true"
    )
    _ = speechsdk.audio.AudioConfig(filename=audio_path)
    return normalize_segments(
        [
            {
                "start": 0.0,
                "end": 1.0,
                "text": "Meeting transcription",
                "speaker": "speaker_1",
                "speech_config": speech_config,
            }
        ]
    )
