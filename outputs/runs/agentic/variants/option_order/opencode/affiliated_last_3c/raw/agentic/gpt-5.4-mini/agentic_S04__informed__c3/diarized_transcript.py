from speech_client import post_json
from speech_models import TranscriptJobRequest


def diarized_transcript(audio_url: str, language_code: str = None):
    request = TranscriptJobRequest(
        audio_url=audio_url, language_code=language_code, diarization=True
    )
    return post_json("/transcript", request.to_payload())
