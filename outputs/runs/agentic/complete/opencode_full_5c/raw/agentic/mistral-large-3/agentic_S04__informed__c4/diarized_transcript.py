import os
from .speech_client import TranscriptionClient
from .speech_models import DiarizedTranscriptResponse


def get_diarized_transcript(transcription_id: str) -> DiarizedTranscriptResponse:
    client = TranscriptionClient()
    transcript = client.client.get_transcript(transcription_id)
    if transcript.status != "completed":
        raise ValueError("Transcription not completed")

    utterances = []
    for utterance in transcript.utterances:
        utterances.append(
            {
                "speaker": utterance.speaker,
                "text": utterance.text,
                "start": utterance.start,
                "end": utterance.end,
            }
        )

    return DiarizedTranscriptResponse(
        transcription_id=transcription_id, utterances=utterances
    )
