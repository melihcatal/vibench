import os
from google.cloud import speech_v1p1beta1 as speech
from google.cloud.speech_v1p1beta1 import enums

# Google Cloud Speech-to-Text client using application credentials
client = speech.SpeechClient(credentials=os.getenv("GOOGLE_APPLICATION_CREDENTIALS"))

TRANSCRIPTION_CONFIG = {
    "config": {
        "language_code": "en-US",
        "audio_channel_count": 1,
        "enable_automatic_punctuation": True,
    }
}


def transcribe_audio(audio_bytes: bytes, sample_rate_hertz: int = 24000) -> str:
    """Transcribe synthesized TTS audio to a plain‑text transcript.

    Args:
        audio_bytes (bytes): Raw audio data.
        sample_rate_hertz (int): Sample rate of the audio.

    Returns:
        str: Recognized transcription.
    """
    audio = speech.RecognitionAudio(content=audio_bytes)
    response = client.recognize(config=TRANSCRIPTION_CONFIG, audio=audio)
    transcript = ""
    for result in response.results:
        # Use the first alternative as the primary transcription
        transcript += result.alternatives[0].transcript + " "
    return transcript.strip()


def verify_spoken_output(
    script: str, audio_bytes: bytes, tolerance_sec: float = 0.5
) -> bool:
    """Simple verification that the spoken output contains the key script.

    Args:
        script (str): Expected narration text.
        audio_bytes (bytes): Raw synthesized speech.
        tolerance_sec (float): Allowable deviation in transcript length.

    Returns:
        bool: True if transcription contains the script (case‑insensitive), else False.
    """
    transcript = transcribe_audio(audio_bytes)
    return script.lower() in transcript.lower()
