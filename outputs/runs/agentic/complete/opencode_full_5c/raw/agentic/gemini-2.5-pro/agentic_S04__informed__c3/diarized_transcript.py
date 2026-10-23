from speech_client import get_speech_client
from speech_models import DiarizedTranscript, TranscriptSegment
from assemblyai import TranscriptionConfig, Transcriber


def get_diarized_transcript(audio_url: str) -> DiarizedTranscript:
    """
    Requests a diarized transcript from AssemblyAI.
    """
    client = get_speech_client()
    config = TranscriptionConfig(speaker_labels=True)
    transcriber = Transcriber(client=client)
    transcript = transcriber.transcribe(audio_url, config)

    if not transcript.utterances:
        return DiarizedTranscript(segments=[])

    segments = [
        TranscriptSegment(
            speaker=utterance.speaker,
            text=utterance.text,
            start=utterance.start,
            end=utterance.end,
        )
        for utterance in transcript.utterances
    ]
    return DiarizedTranscript(segments=segments)
