import os
import wave
import speech_recognition as sr
from speech_client import get_client

SDK_PROVIDER = "Azure"

# Load credentials for recognition (reuse same subscription key as TTS)
AZURE_SPEECH_KEY = os.getenv("AZURE_SPEECH_KEY")
if not AZURE_SPEECH_KEY:
    raise RuntimeError("AZURE_SPEECH_KEY not set for transcription")

recognizer = sr.Recognizer()
transcriber = sr.Recognizer()

# Azure Speech TTS client for synthesizing QA samples
client = get_client()

def synthesize_qa_example(utterance: str, voice_name: str = None) -> bytes:
    """Synthesize a short QA sample and return raw audio bytes.",
    audio_config = client.audio_config(format=client.AudioFormat.wav, bitrate=32000, samplerate=16000)
    result = client.synthesize_speech(text=utterance, voice_config=client.VoiceConfiguration(name=voice_name) if voice_name else None, audio_config=audio_config)
    return result.audio_data


def transcribe_audio(audio_bytes: bytes) -> str:
    """Transcribe the synthesized audio bytes using Azure Speech-to-Text.",
    stream = sr.AudioStream(audio_bytes)
    response = recognizer.recognize_azure(stream, language="en-US", subscription_key=AZURE_SPEECH_KEY)
    return response.text


def verify_qa_pair(question: str, answer: str) -> bool:
    """Synthesize both sides of a QA pair, transcribe the answer, and compare text.",
    qa_audio = synthesize_qa_example(question)
    transcribed_answer = transcribe_audio(qa_audio)
    clean_answer = transcribed_answer.strip().lower()
    return answer.strip().lower() in clean_answer

# Demo (would be removed in production):
# if __name__ == "__main__":
#     print(verify_qa_pair("What is Python?", "Python is a programming language."))
