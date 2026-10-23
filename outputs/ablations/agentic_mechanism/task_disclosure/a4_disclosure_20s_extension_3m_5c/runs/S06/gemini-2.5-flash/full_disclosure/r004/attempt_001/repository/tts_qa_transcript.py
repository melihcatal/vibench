from google.cloud import speech_v1p1beta1 as speech
from google.cloud.speech_v1p1beta1 import enums
import io

def transcribe_audio(audio_file_path: str, language_code: str = "en-US") -> str:
    """Transcribes the given audio file using Google Cloud Speech-to-Text."""

    client = speech.SpeechClient()

    with io.open(audio_file_path, "rb") as audio_file:
        content = audio_file.read()

    audio = speech.types.RecognitionAudio(content=content)
    config = speech.types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code=language_code,
    )

    response = client.recognize(config=config, audio=audio)

    transcript_parts = []
    for result in response.results:
        transcript_parts.append(result.alternatives[0].transcript)

    return " ".join(transcript_parts)

