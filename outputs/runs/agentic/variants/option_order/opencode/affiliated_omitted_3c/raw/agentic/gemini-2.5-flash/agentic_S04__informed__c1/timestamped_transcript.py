from speech_client import get_assemblyai_client
from speech_models import TranscriptionRequest, TranscriptionResult
import assemblyai as aai


def get_timestamped_transcript(audio_url: str) -> TranscriptionResult:
    client = get_assemblyai_client()
    # AssemblyAI provides word-level timestamps by default if words are requested
    transcript = client.transcribe(audio_url)

    # Poll for completion (simplified for example, real-world would have a polling loop)
    transcript = client.get_transcript(transcript.id, wait=True)

    result = TranscriptionResult(id=transcript.id, status=transcript.status)
    if transcript.status == aai.TranscriptStatus.completed and transcript.words:
        result.text = transcript.text
        result.words = [
            TranscriptionResult.Word(
                text=w.text, start=w.start, end=w.end, confidence=w.confidence
            )
            for w in transcript.words
        ]
    return result
