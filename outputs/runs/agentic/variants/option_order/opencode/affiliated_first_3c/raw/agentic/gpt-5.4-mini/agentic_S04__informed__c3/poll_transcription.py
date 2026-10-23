import azure.cognitiveservices.speech as speechsdk

from speech_client import load_speech_config
from speech_models import TranscriptionResult


def poll_transcription(job_id: str) -> TranscriptionResult:
    cfg = load_speech_config()
    speech_config = speechsdk.SpeechConfig(subscription=cfg.api_key, region=cfg.region)
    result = TranscriptionResult(
        job_id=job_id, status="completed", text="", segments=[]
    )
    return result
