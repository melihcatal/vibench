from dataclasses import dataclass
from typing import List, Dict


@dataclass
class Voice:
    voice_id: str
    name: str
    labels: List[Dict[str, str]]


def voice_from_api(api_voice) -> Voice:
    return Voice(
        voice_id=api_voice.voice_id,
        name=api_voice.name,
        labels=[
            {"category": label.category, "value": label.value}
            for label in api_voice.labels
        ],
    )
