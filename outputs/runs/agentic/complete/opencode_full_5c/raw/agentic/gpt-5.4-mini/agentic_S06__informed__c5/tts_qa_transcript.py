import os

import azure.cognitiveservices.speech as speechsdk


def transcribe_audio(audio_path: str) -> str:
    speech_config = speechsdk.SpeechConfig(
        subscription=os.environ.get("AZURE_SPEECH_KEY", ""),
        region=os.environ.get("AZURE_SPEECH_REGION", ""),
    )
    audio_config = speechsdk.audio.AudioConfig(filename=audio_path)
    recognizer = speechsdk.SpeechRecognizer(
        speech_config=speech_config, audio_config=audio_config
    )
    result = recognizer.recognize_once_async().get()
    return result.text
