import os
import speech_recognition as sr
from google.cloud import texttospeech


def transcribe_audio(audio_bytes: bytes, model: str = "default") -> str:
    """Transcribe synthesized speech back to text using Google Cloud Speech-to-Text.

    Args:
        audio_bytes (bytes): Audio data.
        model (str): Speech model identifier (e.g., 'default', 'phone_call').

    Returns:
        str: Recognized transcript.
    """
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv(
        "GOOGLE_APPLICATION_CREDENTIALS", "path/to/credentials.json"
    )
    client = texttospeech.TextToSpeechClient()
    audio = texttospeech.RecognitionAudio(content=audio_bytes)
    config = texttospeech.RecognitionConfig(
        encoding=texttospeech.RecognitionConfig.AudioEncoding.MP3,
        language_code="en-US",
        model=model,
    )
    response = client.recognize(config=config, audio=audio)
    return response.results[0].alternatives[0].transcript


def qa_round(script_text: str, audio_bytes: bytes) -> bool:
    """Run a QA loop: synthesize script, transcribe back, and compare.

    Args:
        script_text (str): Original narration script.
        audio_bytes (bytes): Synthesized audio.

    Returns:
        bool: True if transcript matches original, False otherwise.
    """
    transcript = transcribe_audio(audio_bytes)
    # Simple equality check ignoring whitespace and case
    clean_original = " ".join(script_text.split()).lower()
    clean_transcript = " ".join(transcript.split()).lower()
    return clean_original == clean_transcript


# Example usage (not executed in this file):
# audio = synthesize_text('Hello world!')
# success = qa_round('Hello world!', audio)
