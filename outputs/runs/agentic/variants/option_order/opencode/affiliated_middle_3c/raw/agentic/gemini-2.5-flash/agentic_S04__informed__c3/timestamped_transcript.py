from speech_client import get_assemblyai_client
from speech_models import TranscriptionResult
import assemblyai as aai


def get_timestamped_transcript(transcription_id: str) -> TranscriptionResult:
    client = get_assemblyai_client()
    transcript = client.get_transcript(transcription_id)

    result = TranscriptionResult(
        id=transcript.id, status=transcript.status.value, text=transcript.text
    )
    if transcript.words:
        result.words = [
            {"word": w.text, "start": w.start, "end": w.end, "confidence": w.confidence}
            for w in transcript.words
        ]

    # AssemblyAI also provides utterance-level timestamps if diarization was enabled
    if transcript.utterances:
        result.utterances = [
            {"speaker": u.speaker, "text": u.text, "start": u.start, "end": u.end}
            for u in transcript.utterances
        ]

    return result
