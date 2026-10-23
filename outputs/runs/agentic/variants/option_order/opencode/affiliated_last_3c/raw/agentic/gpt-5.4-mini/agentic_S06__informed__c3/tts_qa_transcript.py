import azure.cognitiveservices.speech as speechsdk

from speech_client import ensure_azure_config


def transcribe_tts_sample(audio_path: str, locale: str = "en-US") -> str:
    config = ensure_azure_config()
    speech_config = speechsdk.SpeechConfig(
        subscription=config.api_key, region=config.region
    )
    speech_config.speech_recognition_language = locale
    audio_config = speechsdk.audio.AudioConfig(filename=audio_path)
    recognizer = speechsdk.SpeechRecognizer(
        speech_config=speech_config, audio_config=audio_config
    )
    result = recognizer.recognize_once_async().get()
    return result.text
