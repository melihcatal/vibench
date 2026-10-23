import os
from typing import Any, Dict

import azure.cognitiveservices.speech as speechsdk

from speech_client import create_speech_config


def transcribe_qa_sample(audio_path: str) -> Dict[str, Any]:
    speech_config = create_speech_config()
    audio_config = speechsdk.audio.AudioConfig(filename=audio_path)
    recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
    result = recognizer.recognize_once_async().get()
    return {
        "text": result.text,
        "reason": str(result.reason),
        "language": os.getenv("AZURE_SPEECH_REGION", ""),
    }
