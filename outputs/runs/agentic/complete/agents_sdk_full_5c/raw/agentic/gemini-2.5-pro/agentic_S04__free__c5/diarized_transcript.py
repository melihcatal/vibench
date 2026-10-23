from typing import List, Dict
from assemblyai import TranscriptionConfig
from speech_client import get_transcriber

def get_diarized_transcript(audio_url: str) -> List[Dict[str, str]]:
    """
    Transcribes an audio file with speaker diarization enabled.

    Args:
        audio_url: The public URL of the audio file.

    Returns:
        A list of utterances, each with a speaker label and text.
    """
    transcriber = get_transcriber()
    config = TranscriptionConfig(speaker_labels=True)
    
    transcript = transcriber.transcribe(audio_url, config=config)

    if transcript.error:
        raise Exception(f"Diarization failed: {transcript.error}")

    if not transcript.utterances:
        return []

    return [
        {"speaker": utterance.speaker, "text": utterance.text}
        for utterance in transcript.utterances
    ]
