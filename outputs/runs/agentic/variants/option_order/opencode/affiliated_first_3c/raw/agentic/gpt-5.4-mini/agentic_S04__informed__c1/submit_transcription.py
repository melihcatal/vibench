import azure.cognitiveservices.speech as speechsdk

from speech_client import require_speech_config
from speech_models import TranscriptionRequest, TranscriptionResponse


def submit_transcription(
    audio_path: str, language: str = "en-US"
) -> TranscriptionResponse:
    config = require_speech_config()
    speech_config = speechsdk.SpeechConfig(
        subscription=config.api_key, region=config.region
    )
    audio = speechsdk.audio.AudioConfig(
        filename=TranscriptionRequest(audio_path=audio_path).audio_path
    )
    recognizer = speechsdk.SpeechRecognizer(
        speech_config=speech_config, audio_config=audio, language=language
    )
    result = recognizer.recognize_once_async().get()
    return TranscriptionResponse(
        job_id="azure-speech-once",
        status=str(result.reason),
        text=result.text,
        raw=result,
    )
