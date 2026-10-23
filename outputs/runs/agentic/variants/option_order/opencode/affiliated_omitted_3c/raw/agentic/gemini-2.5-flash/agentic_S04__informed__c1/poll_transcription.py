from speech_client import get_assemblyai_client
from speech_models import TranscriptionResult
import assemblyai as aai


def poll_transcription_job(job_id: str) -> TranscriptionResult:
    client = get_assemblyai_client()
    transcript = client.get_transcript(job_id)

    result = TranscriptionResult(id=transcript.id, status=transcript.status)
    if transcript.status == aai.TranscriptStatus.completed:
        result.text = transcript.text
        if transcript.words:
            result.words = [
                TranscriptionResult.Word(
                    text=w.text, start=w.start, end=w.end, confidence=w.confidence
                )
                for w in transcript.words
            ]
        if transcript.utterances:
            result.utterances = [
                TranscriptionResult.Utterance(
                    speaker=u.speaker,
                    text=u.text,
                    start=u.start,
                    end=u.end,
                    words=[
                        TranscriptionResult.Word(
                            text=w.text,
                            start=w.start,
                            end=w.end,
                            confidence=w.confidence,
                        )
                        for w in u.words
                    ],
                )
                for u in transcript.utterances
            ]
    return result
