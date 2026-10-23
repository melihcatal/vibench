import os

import azure.cognitiveservices.speech as speechsdk


def transcribe_audio(audio_path: str) -> str:
    speech_config = speechsdk.SpeechConfig(
        subscription=os.getenv("AZURE_SPEECH_KEY", ""),
        region=os.getenv("AZURE_SPEECH_REGION", ""),
    )
    audio_input = speechsdk.audio.AudioConfig(filename=audio_path)
    recognizer = speechsdk.SpeechRecognizer(
        speech_config=speech_config, audio_config=audio_input
    )
    result = recognizer.recognize_once_async().get()
    return result.text
