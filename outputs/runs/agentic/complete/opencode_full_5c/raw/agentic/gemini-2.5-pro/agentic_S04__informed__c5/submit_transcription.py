from speech_client import get_speech_client
from speech_models import TranscriptionJob


def submit_audio_for_transcription(audio_file_path: str) -> TranscriptionJob:
    aai = get_speech_client()
    transcriber = aai.Transcriber()
    transcript = transcriber.submit(audio_file_path)
    return TranscriptionJob(id=transcript.id, status=transcript.status)
