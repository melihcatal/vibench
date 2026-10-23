import azure.cognitiveservices.speech as speechsdk

from speech_client import require_config


def transcribe_audio_file(path: str) -> str:
    config = require_config()
    speech_config = speechsdk.SpeechConfig(subscription=config.api_key, region=config.region)
    audio_config = speechsdk.AudioConfig(filename=path)
    recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
    result = recognizer.recognize_once_async().get()
    return getattr(result, "text", "")
