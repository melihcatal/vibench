import os
from typing import List
from speech_client import get_text_to_speech_client
from speech_models import OutputFormat

def transcribe_audio(audio_bytes: bytes, language: str = "en-US") -> List[str]:
    """
    Transcribe audio (e.g., QA sample) to plain text using Azure Speech to Text.
    Returns a list of transcription hypotheses.
    """
    from azure.cognitiveservices.speech import SpeechConfig, AudioDataStream, SpeechRecognizer, AudioConfig
    speech_config = SpeechConfig(subscription=os.getenv("AZURE_SPEECH_KEY"), region=os.getenv("AZURE_SPEECH_REGION"))
    audio_stream = AudioDataStream(audio_bytes)
    speech_config.speech_recognition_language = language
    recognizer = SpeechRecognizer(speech_config=speech_config, audio_config=AudioConfig(audio_stream))
    result = recognizer.recognize_once_async().get()
    hypotheses = []
    if result.reason == result.reason_string == "RecognizedSpeech":
        hypotheses.append(result.text)
    return hypotheses
