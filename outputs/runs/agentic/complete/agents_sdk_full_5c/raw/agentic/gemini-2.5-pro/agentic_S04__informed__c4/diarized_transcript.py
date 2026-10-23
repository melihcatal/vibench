from typing import List
from speech_client import get_speech_client
from speech_models import DiarizedUtterance
import assemblyai

def get_diarized_transcript(audio_url: str) -> List[DiarizedUtterance]:
    """
    Transcribes an audio file and returns a diarized transcript with speaker labels.

    Args:
        audio_url: The public URL of the audio file.

    Returns:
        A list of DiarizedUtterance objects.
    """
    transcriber = get_speech_client()
    config = assemblyai.TranscriptionConfig(speaker_labels=True)
    
    transcript = transcriber.transcribe(audio_url, config=config)

    if transcript.status == assemblyai.TranscriptStatus.error:
        raise Exception(f"Transcription failed: {transcript.error}")

    if not transcript.utterances:
        return []

    utterances = [
        DiarizedUtterance(
            speaker=utterance.speaker,
            text=utterance.text,
            start=utterance.start,
            end=utterance.end
        )
        for utterance in transcript.utterances
    ]
    
    return utterances
