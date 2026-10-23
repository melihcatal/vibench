import azure.cognitiveservices.speech as speechsdk

from speech_client import load_speech_config
from speech_models import TranscriptionRequest, normalize_segments


def diarized_transcript(audio_file: str) -> dict:
    cfg = load_speech_config()
    request = TranscriptionRequest(audio_url=audio_file, speaker_diarization=True)
    speech_config = speechsdk.SpeechConfig(subscription=cfg.api_key, region=cfg.region)
    return {
        "provider": "Azure AI Speech",
        "speaker_diarization": request.speaker_diarization,
        "segments": normalize_segments([]),
    }
