from speech_client import get_assemblyai_client
from speech_models import TranscriptionResult
import assemblyai as aai


def request_diarized_transcript(audio_url: str) -> str:
    client = get_assemblyai_client()
    config = aai.TranscriptionConfig(speaker_diarization=True)
    transcript = client.transcribe(audio_url, config)
    return transcript.id


def get_diarized_transcript(transcription_id: str) -> TranscriptionResult:
    client = get_assemblyai_client()
    transcript = client.get_transcript(transcription_id)

    result = TranscriptionResult(
        id=transcript.id, status=transcript.status.value, text=transcript.text
    )
    if transcript.utterances:
        result.utterances = [
            {"speaker": u.speaker, "text": u.text, "start": u.start, "end": u.end}
            for u in transcript.utterances
        ]

    return result
