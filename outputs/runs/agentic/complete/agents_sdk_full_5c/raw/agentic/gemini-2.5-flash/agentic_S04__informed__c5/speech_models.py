from typing import List, Dict, Any
import assemblyai

# Helper for common transcription configuration (optional, can be passed directly)
def create_transcription_config(
    audio_url: str,
    speaker_diarization: bool = False,
    word_boost: bool = False,
    **kwargs
) -> assemblyai.TranscriptionConfig:
    """Creates an AssemblyAI TranscriptionConfig object."""
    return assemblyai.TranscriptionConfig(
        audio_url=audio_url,
        speaker_diarization=speaker_diarization,
        word_boost=word_boost,
        **kwargs
    )

# Although AssemblyAI SDK returns rich objects, you might want simple dictionaries
# for further processing or storage. This is a basic example.
def transcript_to_dict(transcript: assemblyai.Transcript) -> Dict[str, Any]:
    """Converts an AssemblyAI Transcript object to a dictionary."""
    return {
        "id": transcript.id,
        "status": transcript.status,
        "text": transcript.text,
        "words": [{
            "text": word.text,
            "start": word.start,
            "end": word.end,
            "speaker": word.speaker
        } for word in transcript.words] if transcript.words else [],
        "speakers": list(set([word.speaker for word in transcript.words if word.speaker])) if transcript.words else []
    }
