# tts_qa_transcript.py
import os
import speech_recognition as sr
import google.cloud.speech_v1p1beta1 as speech

STT_CLIENT = None


def _get_stt_client():
    global STT_CLIENT
    if STT_CLIENT is None:
        STT_CLIENT = speech.SpeechClient()
    return STT_CLIENT


def transcribe_audio(audio_bytes):
    """Transcribe audio bytes using Google Cloud Speech-to-Text (v1p1beta1)."""
    client = _get_stt_client()
    audio = speech.RecognitionAudio(content=audio_bytes)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.MP3,
        language_code="en-US",
        enable_automatic_punctuation=True,
    )
    response = client.recognize(config=config, audio=audio)
    transcript = response.results[0].alternatives[0].transcript
    return transcript
