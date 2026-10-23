# [LATER-STEP] tts_qa_transcript.py
# Transcribe synthesized QA samples to verify spoken output using Google Cloud Speech-to-Text

from google.cloud import speech_v1p1beta1 as speech


def transcribe_audio(audio_bytes: bytes) -> str:
    """Transcribes raw audio bytes into text."""
    client = speech.SpeechClient()
    audio = speech.RecognitionAudio(content=audio_bytes)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        language_code="en-US",
        enable_automatic_punctuation=True,
    )
    response = client.recognize(config=config, audio=audio)
    return response.results[0].alternatives[0].transcript
