from typing import TypedDict, List, Dict, Any, Optional
import assemblyai as aai


class TranscriptResponse(TypedDict):
    job_id: str
    text: str
    words: List[Dict[str, Any]]
    utterances: Optional[List[Dict[str, Any]]]


def get_base_config(diarize: bool = False) -> aai.TranscriptionConfig:
    config = aai.TranscriptionConfig(
        punctuate=True, format_text=True, word_cleaning=True
    )
    config.speaker_labels = diarize
    return config
