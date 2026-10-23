from speech_client import get_assemblyai_client
from speech_models import TranscriptionRequest, TranscriptionResult
import assemblyai as aai


def get_diarized_transcript(audio_url: str) -> TranscriptionResult:
    client = get_assemblyai_client()
    config = aai.TranscriptionConfig(speaker_labels=True)
    transcript = client.transcribe(audio_url, config=config)

    # Poll for completion (simplified for example, real-world would have a polling loop)
    transcript = client.get_transcript(transcript.id, wait=True)

    result = TranscriptionResult(id=transcript.id, status=transcript.status)
    if transcript.status == aai.TranscriptStatus.completed and transcript.utterances:
        result.text = transcript.text
        result.utterances = [
            TranscriptionResult.Utterance(
                speaker=u.speaker,
                text=u.text,
                start=u.start,
                end=u.end,
                words=[
                    TranscriptionResult.Word(
                        text=w.text, start=w.start, end=w.end, confidence=w.confidence
                    )
                    for w in u.words
                ],
            )
            for u in transcript.utterances
        ]
    return result
