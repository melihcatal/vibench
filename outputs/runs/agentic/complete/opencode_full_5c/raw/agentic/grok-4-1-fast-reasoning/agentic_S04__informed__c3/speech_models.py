import os
from typing import Dict, Any, List, Optional
from dataclasses import dataclass


@dataclass
class STTConfig:
    speaker_labels: Optional[bool] = False
    punctuate: Optional[bool] = True
    format_text: Optional[bool] = True

    def to_api_params(self) -> Dict[str, Any]:
        params = {}
        for field in self.__dataclass_fields__.keys():
            value = getattr(self, field)
            if value is not None:
                params[field] = value
        return params


def parse_diarized_transcript(result: Dict[str, Any]) -> List[Dict[str, Any]]:
    return [
        {
            "speaker": utterance["speaker"],
            "start": utterance["start"],
            "end": utterance["end"],
            "text": utterance["text"],
        }
        for utterance in result.get("utterances", [])
    ]


def parse_timestamped_transcript(result: Dict[str, Any]) -> List[Dict[str, Any]]:
    return [
        {
            "text": word["text"],
            "start": word["start"],
            "end": word["end"],
            "confidence": word.get("confidence"),
        }
        for word in result.get("words", [])
    ]
