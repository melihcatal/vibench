# Utilities for request/response handling and normalization for the streaming API.
import json
from typing import Any, Dict, List
from google.cloud.speech_v1p1beta1 import types


class StreamResponseHandler:
    """Simple container to collect incremental results from the streaming API."""
    def __init__(self) -> None:
        self.final_transcripts: Dict[str, str] = {}

    def handle(self, result: types.StreamingRecognizeResult) -> None:
        if result.is_final:
            self.final_transcripts[result.result_index] = result.alternatives[0].transcript
        # interim results can be ignored here
    
    def get_final(self) -> Dict[str, str]:
        return self.final_transcripts
    
    def get_all(self) -> List[str]:
        return list(self.final_transcripts.values())

# Normalizer for transcript strings
WHITESPACE_NORM = str.maketrans({"\n": " ", "\t": " "})

def normalize(text: str) -> str:
    """Collapse newlines/tabs and strip surrounding spaces."""
    return text.translate(WHITESPACE_NORM).strip()

__all__ = ["StreamResponseHandler", "normalize"]
