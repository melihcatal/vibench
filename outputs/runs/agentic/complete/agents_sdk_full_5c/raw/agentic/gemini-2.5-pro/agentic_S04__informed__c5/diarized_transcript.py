from typing import List
from speech_client import get_speech_client
from speech_models import Utterance


def get_diarized_transcript(audio_url: str) -> List[Utterance]:
    """
    Transcribes an audio file with speaker diarization enabled.

    Args:
        audio_url: The public URL of the audio file.

    Returns:
        A list of utterances with speaker labels.
    """
    aai = get_speech_client()
    transcriber = aai.Transcriber()

    config = aai.TranscriptionConfig(speaker_labels=True)
    transcript = transcriber.transcribe(audio_url, config)

    if transcript.status == "error":
        raise RuntimeError(f"Transcription failed: {transcript.error}")

    if not transcript.utterances:
        return []

    return [
        Utterance(
            start=utt.start,
            end=utt.end,
            text=utt.text,
            speaker=utt.speaker
        )
        for utt in transcript.utterances
    ]
