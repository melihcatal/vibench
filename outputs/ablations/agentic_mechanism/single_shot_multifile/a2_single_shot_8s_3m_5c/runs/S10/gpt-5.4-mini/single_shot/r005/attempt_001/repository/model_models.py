from __future__ import annotations

from dataclasses import dataclass
import json
from typing import Any


@dataclass
class BuildTextRequest:
    task: str
    input_text: str
    max_sentences: int | None = None
    schema_hint: str | None = None

    def to_prompt(self) -> str:
        parts = [f"Task: {self.task}", f"Input: {self.input_text}"]
        if self.max_sentences is not None:
            parts.append(f"Max sentences: {self.max_sentences}")
        if self.schema_hint:
            parts.append(f"Schema hint: {self.schema_hint}")
        return "\n".join(parts)


@dataclass
class QARequest:
    question: str
    context: str

    def to_prompt(self) -> str:
        return f"Context:\n{self.context}\n\nQuestion: {self.question}"


@dataclass
class StreamPromptRequest:
    prompt: str


@dataclass
class BaseTextResult:
    text: str
    model: str

    @classmethod
    def from_text(cls, text: str, model: str):
        return cls(text=text, model=model)


@dataclass
class SummarizeResult(BaseTextResult):
    pass


@dataclass
class QAResult(BaseTextResult):
    pass


@dataclass
class JsonExtractionResult:
    data: Any
    model: str

    @classmethod
    def from_text(cls, text: str, model: str):
        try:
            data = json.loads(text)
        except Exception:
            data = {"raw": text}
        return cls(data=data, model=model)
