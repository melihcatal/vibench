from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class ChatMessage:
    role: str
    content: str


@dataclass(frozen=True)
class ChatRequest:
    task: str
    model: str
    system_prompt: str
    user_prompt: str

    def messages(self) -> List[dict]:
        return [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": self.user_prompt},
        ]


def normalize_text(text: str) -> str:
    return " ".join(text.split())
