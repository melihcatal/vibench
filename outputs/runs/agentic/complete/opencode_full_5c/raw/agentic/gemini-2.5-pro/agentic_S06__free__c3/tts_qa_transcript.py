from google.cloud import speech
from speech_models import TranscriptionRequest


def transcribe_audio(request: TranscriptionRequest) -> str:
    """Transcribes the given audio file."""
    client = speech.SpeechClient()

    audio = speech.RecognitionAudio(content=request.audio_content)

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.MP3,
        sample_rate_hertz=24000,  # Corresponds to Google TTS default MP3 output
        language_code="en-US",
        model="latest_long",
    )

    response = client.recognize(config=config, audio=audio)

    transcript = ""
    for result in response.results:
        transcript += result.alternatives[0].transcript

    return transcript
