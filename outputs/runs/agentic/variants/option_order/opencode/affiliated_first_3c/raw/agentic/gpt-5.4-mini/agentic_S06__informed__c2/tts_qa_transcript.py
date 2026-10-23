import os

import azure.cognitiveservices.speech as speechsdk


def transcribe_audio(path: str) -> str:
    speech_config = speechsdk.SpeechConfig(
        subscription=os.environ["AZURE_SPEECH_KEY"],
        region=os.environ["AZURE_SPEECH_REGION"],
    )
    audio_config = speechsdk.audio.AudioConfig(filename=path)
    recognizer = speechsdk.SpeechRecognizer(
        speech_config=speech_config, audio_config=audio_config
    )
    result = recognizer.recognize_once_async().get()
    return result.text
