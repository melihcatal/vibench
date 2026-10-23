from speech_client import get_assemblyai_client
from speech_models import TranscriptionRequest, TranscriptionResult


def submit_transcription_job(request: TranscriptionRequest) -> TranscriptionResult:
    client = get_assemblyai_client()
    config = aai.TranscriptionConfig(
        speaker_labels=request.diarize, word_boost=request.word_boost
    )
    transcript = client.transcriber.transcribe(request.audio_url, config=config)
    return TranscriptionResult(id=transcript.id, status=transcript.status.value)
