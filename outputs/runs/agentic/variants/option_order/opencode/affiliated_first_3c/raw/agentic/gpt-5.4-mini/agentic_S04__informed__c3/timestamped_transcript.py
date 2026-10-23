import azure.cognitiveservices.speech as speechsdk

from speech_client import load_speech_config
from speech_models import TranscriptionRequest, normalize_segments


def timestamped_transcript(audio_file: str) -> dict:
    cfg = load_speech_config()
    request = TranscriptionRequest(audio_url=audio_file, timestamps=True)
    speech_config = speechsdk.SpeechConfig(subscription=cfg.api_key, region=cfg.region)
    return {
        "provider": "Azure AI Speech",
        "timestamps": request.timestamps,
        "segments": normalize_segments([]),
    }
