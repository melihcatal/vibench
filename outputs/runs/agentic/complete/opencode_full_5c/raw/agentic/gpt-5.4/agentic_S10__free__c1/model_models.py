from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional


@dataclass
class ChatTurn:
    role: str
    content: str

    def to_dict(self) -> Dict[str, str]:
        return {"role": self.role, "content": self.content}


@dataclass
class GenerationRequest:
    instructions: str
    input_text: str
    model: Optional[str] = None
    temperature: float = 0.2
    max_output_tokens: int = 500

    def user_prompt(self) -> str:
        return self.input_text.strip()

    def system_prompt(self) -> str:
        return self.instructions.strip()


@dataclass
class AnswerWithContextRequest:
    question: str
    context: str
    model: Optional[str] = None
    temperature: float = 0.1
    max_output_tokens: int = 400

    def messages(self) -> List[ChatTurn]:
        return [
            ChatTurn(
                role="system",
                content="Answer the question using only the supplied context. If the context is insufficient, say so clearly.",
            ),
            ChatTurn(
                role="user",
                content=f"Context:\n{self.context.strip()}\n\nQuestion:\n{self.question.strip()}",
            ),
        ]


@dataclass
class CompletionResult:
    text: str
    model: str
    provider: str
    usage: Dict[str, Any]


def normalize_messages(messages: Iterable[ChatTurn]) -> List[Dict[str, str]]:
    return [message.to_dict() for message in messages]


def coerce_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    return str(value).strip()


def build_json_extraction_prompt(schema_hint: str, text: str) -> str:
    return (
        "Extract structured data from the source text and return only valid JSON that matches this schema guidance:\n"
        f"{schema_hint.strip()}\n\n"
        "Source text:\n"
        f"{text.strip()}"
    )


def package_result(
    text: str, model: str, usage: Optional[Dict[str, Any]] = None
) -> CompletionResult:
    return CompletionResult(
        text=coerce_text(text),
        model=model,
        provider="openai",
        usage=usage or {},
    )
