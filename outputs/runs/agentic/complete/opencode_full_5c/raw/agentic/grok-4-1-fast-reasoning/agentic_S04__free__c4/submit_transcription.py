from typing import Optional
from speech_client import get_speech_client


def submit_transcription(
    audio_file: str, language_code: str = "en", api_key: Optional[str] = None
) -> str:
    client = get_speech_client(api_key)
    transcript = client.transcripts.create(
        audio_url=audio_file, language_code=language_code
    )
    return transcript.id
