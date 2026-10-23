from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class StreamingCaption:
    text: str
    is_final: bool = False
    language: Optional[str] = None


def normalize_caption_text(text: str) -> str:
    return " ".join(text.split()).strip()


def build_caption_payload(text: str, is_final: bool = False, language: Optional[str] = None) -> Dict[str, Any]:
    return {"text": normalize_caption_text(text), "is_final": is_final, "language": language}


def captions_from_events(events: List[Dict[str, Any]]) -> List[StreamingCaption]:
    captions: List[StreamingCaption] = []
    for event in events:
        captions.append(
            StreamingCaption(
                text=normalize_caption_text(str(event.get("text", ""))),
                is_final=bool(event.get("is_final", False)),
                language=event.get("language"),
            )
        )
    return captions
