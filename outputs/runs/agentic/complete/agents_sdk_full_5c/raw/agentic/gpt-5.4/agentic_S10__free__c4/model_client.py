from __future__ import annotations

import os
from typing import Iterable, Iterator, List

from openai import OpenAI

from model_models import ChatTurn, InferenceRequest, NormalizedTextResult


DEFAULT_TEXT_MODEL = os.getenv("OPENAI_TEXT_MODEL", "gpt-4o-mini")
DEFAULT_REASONING_MODEL = os.getenv("OPENAI_REASONING_MODEL", "gpt-4.1-mini")
DEFAULT_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
DEFAULT_MODERATION_MODEL = os.getenv("OPENAI_MODERATION_MODEL", "omni-moderation-latest")
DEFAULT_TTS_MODEL = os.getenv("OPENAI_TTS_MODEL", "gpt-4o-mini-tts")
DEFAULT_TTS_VOICE = os.getenv("OPENAI_TTS_VOICE", "alloy")


class HostedModelClient:
    def __init__(self, api_key: str | None = None, base_url: str | None = None) -> None:
        self.client = OpenAI(
            api_key=api_key or os.getenv("OPENAI_API_KEY"),
            base_url=base_url or os.getenv("OPENAI_BASE_URL"),
        )

    def choose_model_family(self, task: str) -> str:
        task_key = task.strip().lower()
        if task_key in {"reasoning", "json", "qa", "answer"}:
            return DEFAULT_REASONING_MODEL
        return DEFAULT_TEXT_MODEL

    def build_request(
        self,
        task: str,
        system_prompt: str,
        user_prompt: str,
        *,
        temperature: float = 0.2,
        max_tokens: int | None = None,
    ) -> InferenceRequest:
        return InferenceRequest(
            model=self.choose_model_family(task),
            messages=[
                ChatTurn(role="system", content=system_prompt),
                ChatTurn(role="user", content=user_prompt),
            ],
            temperature=temperature,
            max_tokens=max_tokens,
            metadata={"task": task, "provider": "openai"},
        )

    def generate(self, request: InferenceRequest) -> NormalizedTextResult:
        response = self.client.chat.completions.create(**request.as_openai_payload())
        choice = response.choices[0]
        return NormalizedTextResult(
            text=(choice.message.content or "").strip(),
            model=response.model,
            finish_reason=choice.finish_reason,
            raw=response,
        )

    def stream_text(self, request: InferenceRequest) -> Iterator[str]:
        stream = self.client.chat.completions.create(**request.as_openai_payload(), stream=True)
        for event in stream:
            if not event.choices:
                continue
            delta = event.choices[0].delta.content
            if delta:
                yield delta


def join_text(parts: Iterable[str]) -> str:
    return "".join(parts)


def ensure_messages(context: str, question: str) -> List[ChatTurn]:
    return [
        ChatTurn(role="system", content="Answer using only the supplied context. If the answer is absent, say so plainly."),
        ChatTurn(role="user", content=f"Context:\n{context.strip()}\n\nQuestion: {question.strip()}"),
    ]
