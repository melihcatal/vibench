from speech_client import get_assemblyai_client
from speech_models import TranscriptionJob


def submit_transcription_job(audio_file_path: str) -> TranscriptionJob:
    """
    Submits an audio file to AssemblyAI for transcription.
    """
    aai = get_assemblyai_client()
    transcriber = aai.Transcriber()
    transcript = transcriber.submit(audio_file_path)
    return TranscriptionJob(id=transcript.id, status=transcript.status)
