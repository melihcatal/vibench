from speech_client import get_speech_to_text_client
from speech_models import TranscribeAudioRequest
from google.cloud import speech_v1p1beta1 as speech
from typing import List


def transcribe_audio(
    audio_content: bytes, language_code: str, sample_rate_hertz: int = None
) -> List[str]:
    client = get_speech_to_text_client()

    audio = speech.RecognitionAudio(content=audio_content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,  # Assuming raw audio bytes, might need to adjust based on source
        sample_rate_hertz=sample_rate_hertz,
        language_code=language_code,
    )

    response = client.recognize(config=config, audio=audio)

    transcripts = []
    for result in response.results:
        transcripts.append(result.alternatives[0].transcript)
    return transcripts
