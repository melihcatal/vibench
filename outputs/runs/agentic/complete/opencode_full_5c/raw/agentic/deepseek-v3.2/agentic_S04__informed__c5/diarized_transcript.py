import os
import assemblyai as aai
from speech_client import get_speech_client


def diarized_transcript(audio_url: str, speaker_count: int = None) -> str:
    """Request speaker diarization for a recorded meeting using AssemblyAI."""
    client = get_speech_client()

    config = aai.TranscriptionConfig(
        speaker_labels=True,
        speakers_expected=speaker_count,
        speech_model=aai.SpeechModel.best,
    )

    transcript = client.transcribe(audio_url, config=config)

    if transcript.status == aai.TranscriptStatus.error:
        raise Exception(f"Diarization failed: {transcript.error}")

    diarized_text = ""
    if transcript.utterances:
        for utterance in transcript.utterances:
            speaker_label = f"Speaker {utterance.speaker}"
            diarized_text += f"{speaker_label}: {utterance.text}\n"

    return diarized_text, transcript.id
