import os
from google.cloud import speech


def transcribe_audio_for_qa(audio_content: bytes, language_code: str = "en-US") -> str:
    """Transcribes synthesized QA samples to verify spoken output using Google Cloud Speech-to-Text."""
    client = speech.SpeechClient()

    audio = client.RecognitionAudio(content=audio_content)
    config = client.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,  # Assuming LINEAR16 encoding for the input bytes
        sample_rate_hertz=16000,  # This might need to be adjusted based on the actual audio content's sample rate
        language_code=language_code,
    )

    response = client.recognize(config=config, audio=audio)

    transcript_parts = []
    for result in response.results:
        transcript_parts.append(result.alternatives[0].transcript)

    return " ".join(transcript_parts)
