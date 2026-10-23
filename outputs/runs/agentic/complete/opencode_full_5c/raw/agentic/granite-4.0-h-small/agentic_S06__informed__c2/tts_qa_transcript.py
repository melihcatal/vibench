# [LATER-STEP] tts_qa_transcript.py
# Transcribe synthesized QA samples to verify spoken output using Azure Speech to Text

import os
from azure.cognitiveservices.speech import (
    SpeechConfig,
    AudioDataStream,
    SpeechRecognizer,
    ResultReason,
)

AZURE_SPEECH_KEY = os.getenv("AZURE_SPEECH_KEY")
AZURE_SPEECH_REGION = os.getenv("AZURE_SPEECH_REGION")

if not (AZURE_SPEECH_KEY and AZURE_SPEECH_REGION):
    raise RuntimeError("Azure Speech credentials missing")


def transcribe_audio(audio_bytes: bytes) -> str:
    """Transcribe raw audio (PCM or WAV) to text using Azure Speech to Text.

    Args:
        audio_bytes (bytes): The audio data produced by a synthesizer.

    Returns:
        str: The recognized spoken text (lowercased for simple verification).
    """
    speech_config = SpeechConfig(
        subscription=AZURE_SPEECH_KEY, region=AZURE_SPEECH_REGION
    )
    # Use default recognition language; adjust per locale if needed
    speech_config.speech_recognition_language = "en-US"
    audio_input = AudioDataStream(audio_bytes)
    recognizer = SpeechRecognizer(speech_config=speech_config, audio_input=audio_input)
    result = recognizer.recognize_once()
    if result.reason == ResultReason.RecognizedSpeech:
        transcript = result.text
        return transcript.strip().lower()
    elif result.reason == ResultReason.NoMatch:
        raise ValueError("No speech detected in the audio stream.")
    else:
        raise RuntimeError(f"Recognition error: {result.reason}")


# Example usage (requires audio bytes from earlier synthesis step)
if __name__ == "__main__":
    # Placeholder: replace with real audio bytes from your synthesis workflow
    placeholder_audio = b"placeholder"
    try:
        transcript = transcribe_audio(placeholder_audio)
        print("Transcribed text:", transcript)
    except Exception as e:
        print("Transcription failed:", e)
