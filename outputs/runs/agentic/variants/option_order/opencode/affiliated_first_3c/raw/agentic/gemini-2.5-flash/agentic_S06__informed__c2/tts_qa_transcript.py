import os
from google.cloud import speech


def transcribe_audio(
    audio_content: bytes, language_code: str = "en-US", sample_rate_hertz: int = 16000
) -> str:
    """Transcribes synthesized QA samples using Google Cloud Speech-to-Text to verify spoken output.

    Args:
        audio_content: The audio content as bytes.
        language_code: The language of the supplied audio (e.g., "en-US").
        sample_rate_hertz: The sample rate in Hertz of the audio content.

    Returns:
        The transcribed text.
    """
    client = speech.SpeechClient()

    audio = speech.RecognitionAudio(content=audio_content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,  # Assuming LINEAR16 from TTS output for simplicity
        sample_rate_hertz=sample_rate_hertz,
        language_code=language_code,
    )

    # GOOGLE_APPLICATION_CREDENTIALS environment variable is expected for authentication
    response = client.recognize(config=config, audio=audio)

    transcript = ""
    for result in response.results:
        transcript += result.alternatives[0].transcript

    return transcript
