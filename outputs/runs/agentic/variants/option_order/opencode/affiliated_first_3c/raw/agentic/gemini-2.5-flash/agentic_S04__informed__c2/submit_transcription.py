from speech_client import SpeechClient
from speech_models import TranscriptionRequest, TranscriptionResponse


def submit_transcription(audio_url: str) -> TranscriptionResponse:
    speech_client = SpeechClient()
    # AssemblyAI's create method handles the submission
    config = {"audio_url": audio_url}
    # The actual AssemblyAI API call
    transcript = speech_client.client.transcripts.create(audio_url=audio_url)
    return TranscriptionResponse(id=transcript.id, status=transcript.status.value)
