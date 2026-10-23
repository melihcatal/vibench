# [LATER-STEP] tts_qa_transcript.py

import os
from google.cloud import speech_v1p1beta1 as speech

# Load Speech-to-Text client (requires GOOGLE_APPLICATION_CREDENTIALS)
client = speech.SpeechClient()


def transcribe_audio(audio_bytes: bytes, language_code: str = "en-US") -> str:
    """Transcribes synthesized speech audio to text using Google Cloud Speech-to-Text.

    Note: this call charges based on audio duration.

    Args:
        audio_bytes: Raw audio (e.g., bytes returned from synthesize_text).
        language_code: BCP-47 language tag; matching the synthesis language.

    Returns:
        A plain‑text transcription of the audio.
    """
    audio = speech.RecognitionAudio(content=audio_bytes)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=24000,  # reasonable default for TTS output
        language_code=language_code,
        enable_automatic_punctuation=True,
    )
    response = client.recognize(config=config, audio=audio)
    transcript = response.results[0].alternatives[0].transcript.strip()
    return transcript


# Example usage (requires saved audio file):
# with open("output.mp3", "rb") as f:
#     audio = f.read()
# print(transcribe_audio(audio))
