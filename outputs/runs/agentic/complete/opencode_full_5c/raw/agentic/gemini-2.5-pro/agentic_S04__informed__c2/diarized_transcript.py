from typing import List
from speech_client import get_assemblyai_client
from speech_models import TranscriptionResult, Utterance


def get_diarized_transcript(audio_file_path: str) -> TranscriptionResult:
    """
    Submits a job with speaker diarization and returns the diarized transcript.
    """
    aai = get_assemblyai_client()
    config = aai.TranscriptionConfig(speaker_labels=True)
    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(audio_file_path, config)

    if transcript.status == "error":
        return TranscriptionResult(
            id=transcript.id, status=transcript.status, text=transcript.error
        )

    utterances = []
    if transcript.utterances:
        for utterance in transcript.utterances:
            utterances.append(
                Utterance(
                    text=utterance.text,
                    start=utterance.start,
                    end=utterance.end,
                    speaker=utterance.speaker,
                    words=[],  # Words are not needed for this high-level result
                )
            )

    return TranscriptionResult(
        id=transcript.id, status=transcript.status, utterances=utterances
    )
