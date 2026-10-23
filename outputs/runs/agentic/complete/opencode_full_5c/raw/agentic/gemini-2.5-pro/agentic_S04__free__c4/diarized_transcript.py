from speech_client import SpeechClient
from speech_models import TranscriptionResponse


def request_diarized_transcript(audio_url: str) -> TranscriptionResponse:
    """
    Requests speaker diarization for a recorded meeting from AssemblyAI.
    """
    client = SpeechClient()
    response = client.submit_transcription(audio_url, speaker_labels=True)
    return response
