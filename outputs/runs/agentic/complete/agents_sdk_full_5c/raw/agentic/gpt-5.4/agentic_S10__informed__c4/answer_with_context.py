from __future__ import annotations

from typing import Iterable, List

from model_client import build_generation_config, create_chat_completion, extract_text_and_usage
from model_models import AnswerResult, ChatMessage, trim_text


def answer_with_context(question: str, context_chunks: Iterable[str]) -> AnswerResult:
    cleaned_chunks: List[str] = [trim_text(chunk, 4000) for chunk in context_chunks if chunk and chunk.strip()]
    compiled_context = "\n\n".join(f"[Source {idx + 1}] {chunk}" for idx, chunk in enumerate(cleaned_chunks))
    messages = [
        ChatMessage(role="system", content="Answer only using the provided context. If the answer is not in context, say so clearly."),
        ChatMessage(
            role="user",
            content=(
                f"Question: {question}\n\n"
                "Context:\n"
                f"{compiled_context}\n\n"
                "Answer the question and cite the relevant source labels."
            ),
        ),
    ]
    response = create_chat_completion(
        messages,
        config=build_generation_config(model="gpt-4o-mini", temperature=0.1, max_tokens=350),
    )
    parsed = extract_text_and_usage(response)
    citations = [f"Source {idx + 1}" for idx, _ in enumerate(cleaned_chunks) if f"Source {idx + 1}" in parsed["text"]]
    return AnswerResult(answer=parsed["text"], model=parsed["model"], citations=citations, usage=parsed["usage"])
