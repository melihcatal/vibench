from typing import Optional
from speech_client import get_speech_client


def submit_diarized_transcription(
    audio_file: str,
    language_code: str = "en",
    speakers_expected: Optional[int] = None,
    api_key: Optional[str] = None,
) -> str:
    client = get_speech_client(api_key)
    kwargs = {
        "audio_url": audio_file,
        "language_code": language_code,
        "speaker_labels": True,
    }
    if speakers_expected:
        kwargs["speakers_expected"] = speakers_expected
    transcript = client.transcripts.create(**kwargs)
    return transcript.id
