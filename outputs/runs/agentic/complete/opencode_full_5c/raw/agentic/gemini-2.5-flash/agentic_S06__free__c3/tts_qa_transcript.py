from google.cloud import speech_v1p1beta1 as speech
from speech_client import get_speech_to_text_client
from speech_models import TranscriptionOutput
from io import BytesIO


def transcribe_audio(
    audio_content: bytes, language_code: str = "en-US"
) -> TranscriptionOutput:
    client = get_speech_to_text_client()

    audio = speech.RecognitionAudio(content=audio_content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,  # Assuming LINEAR16 from TTS output
        sample_rate_hertz=24000,  # Common sample rate for TTS, adjust if needed
        language_code=language_code,
    )

    response = client.recognize(config=config, audio=audio)

    transcript = ""
    confidence = 0.0
    if response.results:
        # Take the first alternative of the first result
        first_result = response.results[0]
        if first_result.alternatives:
            first_alternative = first_result.alternatives[0]
            transcript = first_alternative.transcript
            confidence = first_alternative.confidence

    return TranscriptionOutput(transcript=transcript, confidence=confidence)
