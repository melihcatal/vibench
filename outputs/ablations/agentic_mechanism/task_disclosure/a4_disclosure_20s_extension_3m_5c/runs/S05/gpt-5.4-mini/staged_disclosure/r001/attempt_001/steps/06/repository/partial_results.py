from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class PartialRecognitionState:
    provider: str = "assemblyai"
    partial_text: str = ""
    final_text: str = ""
    partials: List[str] = field(default_factory=list)
    finals: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def apply_event(self, event: Dict[str, Any]) -> Optional[str]:
        event_type = event.get("type") or event.get("event") or event.get("status")
        text = event.get("text") or event.get("transcript") or ""
        if not text and isinstance(event.get("result"), dict):
            text = event["result"].get("text", "")

        if event_type in {"partial", "interim", "in_progress", "transcript.partial"}:
            self.partial_text = text
            if text:
                self.partials.append(text)
            return self.partial_text

        if event_type in {"final", "completed", "recognized", "transcript.final"}:
            if text:
                self.finals.append(text)
                self.final_text = (self.final_text + " " + text).strip() if self.final_text else text
            self.partial_text = ""
            return self.final_text

        if event_type == "error":
            raise ValueError(event.get("message") or event.get("error") or "Streaming recognition error")

        if text:
            self.partial_text = text
            self.partials.append(text)
            return self.partial_text

        return None

    def snapshot(self) -> Dict[str, Any]:
        return {
            "provider": self.provider,
            "partial_text": self.partial_text,
            "final_text": self.final_text,
            "partials": list(self.partials),
            "finals": list(self.finals),
            "metadata": dict(self.metadata),
        }


def handle_streaming_event(state: PartialRecognitionState, event: Any) -> Optional[str]:
    if isinstance(event, str):
        event = json.loads(event)
    if not isinstance(event, dict):
        raise TypeError("event must be a dict or JSON string")
    state.metadata.update({k: v for k, v in event.items() if k not in {"type", "event", "status", "text", "transcript", "result", "message", "error"}})
    return state.apply_event(event)


def create_state() -> PartialRecognitionState:
    return PartialRecognitionState()
