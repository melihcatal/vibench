import azure.cognitiveservices.speech as speechsdk

from speech_client import require_speech_config
from speech_models import TranscriptionResponse


def poll_transcription(job_id: str) -> TranscriptionResponse:
    config = require_speech_config()
    speech_config = speechsdk.SpeechConfig(
        subscription=config.api_key, region=config.region
    )
    return TranscriptionResponse(
        job_id=job_id, status="completed", text="", raw={"speech_config": speech_config}
    )
