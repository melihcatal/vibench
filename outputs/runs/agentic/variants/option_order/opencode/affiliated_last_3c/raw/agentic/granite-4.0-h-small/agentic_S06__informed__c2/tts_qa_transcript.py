# [LATER-STEP] tts_qa_transcript.py
# Transcribe synthesized QA samples to verify spoken output using Google Cloud Speech-to-Text
import os
from google.cloud import speech_v1p1beta1 as speech
import io

goog_creds = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
if not goog_creds:
    raise RuntimeError("Set GOOGLE_APPLICATION_CREDENTIALS env var for GCP")


def transcribe_audio(audio_bytes: bytes) -> str:
    """Transcribe raw audio bytes to text using Google Speech-to-Text."""
    client = speech.SpeechClient()
    audio = speech.RecognitionAudio(content=audio_bytes)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=24000,  # adjust to your synthesis sample rate
        language_code="en-US",
        enable_automatic_punctuation=True,
    )
    response = client.recognize(config=config, audio=audio)
    transcript = ""
    for result in response.results:
        alt = result.alternatives[0]
        transcript += alt.transcript + "\n"
    return transcript


# Example usage (requires a generated audio file or bytes)
if __name__ == "__main__":
    # Placeholder: assume `synthesized.wav` already exists as a temporary file
    audio_path = "synthesized.wav"
    with io.open(audio_path, "rb") as f:
        audio_bytes = f.read()
    print("Transcript:", transcribe_audio(audio_bytes))
