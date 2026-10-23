from speech_client import get_assemblyai_client
from speech_models import TranscriptionRequest, TranscriptionResult


def request_diarized_transcript(audio_url: str):
    client = get_assemblyai_client()
    config = client.TranscriptionConfig(speaker_diarization=True)
    transcript = client.transcribe(audio_url, config)
    return TranscriptionResult(
        id=transcript.id,
        status=transcript.status,
        text=transcript.text,
        utterances=transcript.utterances,
    )
