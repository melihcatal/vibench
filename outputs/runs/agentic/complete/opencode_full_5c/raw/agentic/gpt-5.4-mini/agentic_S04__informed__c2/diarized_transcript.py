from speech_client import build_transcriber, response_to_result
from speech_models import TranscriptionRequest


def diarized_transcript(audio_url: str, language_code: str = None):
    transcriber = build_transcriber()
    request = TranscriptionRequest(
        audio_url=audio_url, language_code=language_code, speaker_labels=True
    )
    job = transcriber.transcribe(
        audio_url, speaker_labels=True, language_code=language_code
    )
    return response_to_result(job)
