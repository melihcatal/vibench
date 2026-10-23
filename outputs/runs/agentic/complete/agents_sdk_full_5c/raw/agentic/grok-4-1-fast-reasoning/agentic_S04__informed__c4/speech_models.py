import assemblyai as aai
from typing import Optional, List

def create_transcription_config(
    speaker_labels: bool = False,
    punctuate: bool = True,
    format_text: bool = True,
    word_boost: Optional[List[str]] = None
) -> aai.TranscriptionConfig:
    config = aai.TranscriptionConfig(
        speaker_labels=speaker_labels,
        punctuate=punctuate,
        format_text=format_text,
        word_boost=word_boost or []
    )
    return config