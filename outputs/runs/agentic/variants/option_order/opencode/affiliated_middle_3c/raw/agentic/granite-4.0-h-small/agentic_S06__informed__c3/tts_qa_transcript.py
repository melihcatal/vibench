# LATER-STEP: tts_qa_transcript.py
# Transcribe synthesized QA audio samples using Azure AI Speech to verify output

import os
import azure.cognitiveservices.speech as speechsdk
from typing import List

# Configuration via environment variables
AZURE_SPEECH_KEY = os.getenv("AZURE_SPEECH_KEY")
AZURE_SPEECH_REGION = os.getenv("AZURE_SPEECH_REGION")

if not AZURE_SPEECH_KEY or not AZURE_SPEECH_REGION:
    raise RuntimeError("AZURE_SPEECH_KEY and AZURE_SPEECH_REGION must be set")

# Initialize speech config
speech_config = speechsdk.SpeechConfig(
    subscription=AZURE_SPEECH_KEY, region=AZURE_SPEECH_REGION
)


def transcribe_audio(audio_bytes: bytes) -> str:
    """Transcribe raw audio bytes to plain text using Azure Speech to Text.

    Returns the best recognized text.
    """
    audio_config = speechsdk.audio.AudioConfig(audio_data=audio_bytes)
    speech_recognizer = speechsdk.SpeechRecognizer(
        speech_config=speech_config, audio_config=audio_config
    )
    result = speech_recognizer.recognize_once()
    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        return result.text
    elif result.reason == speechsdk.ResultReason.NoMatch:
        return "No speech recognized"
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancelled = result.cancellation_details
        return f"Canceled: {cancelled.reason} - {cancelled.error_details}"
    else:
        return "Unexpected recognition result"


# Example usage (requires AZURE keys)
if __name__ == "__main__":
    # Assume we have synthesized audio from previous steps saved to file
    with open("sample_output.flac", "rb") as f:
        audio = f.read()
    transcript = transcribe_audio(audio)
    print("Transcribed QA sample:", transcript)
