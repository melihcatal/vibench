from speech_client import get_assemblyai_client
import assemblyai as aai
from typing import List, Dict

def get_diarized_transcript(audio_url: str) -> List[Dict[str, str]]:
    """
    Transcribes an audio file with speaker diarization enabled.
    This is a blocking call that waits for the transcript to complete.
    """
    aai_client = get_assemblyai_client()
    transcriber = aai_client.Transcriber()
    
    config = aai.TranscriptionConfig(speaker_labels=True)
    
    transcript = transcriber.transcribe(audio_url, config)

    if transcript.status == aai.TranscriptStatus.error:
        raise RuntimeError(f"Transcription failed: {transcript.error}")

    if not transcript.utterances:
        return []

    return [
        {"speaker": utterance.speaker, "text": utterance.text}
        for utterance in transcript.utterances
    ]
