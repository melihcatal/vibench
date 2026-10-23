"""
answer_with_context.py — calls a hosted LLM (OpenAI gpt-4o) to answer a
question using provided context.

Uses the OpenAI Chat Completions API (api.openai.com) with the
gpt-4o-2024-08-06 model for grounded question answering.
"""

from __future__ import annotations

from typing import Optional

from model_client import run_completion, resolve_model
from model_models import build_chat_request, CompletionResponse

# Concrete OpenAI model identifier for contextual QA
QA_MODEL = resolve_model("gpt-4o")  # gpt-4o-2024-08-06

QA_SYSTEM_PROMPT = (
    "You are a helpful assistant that answers questions based strictly on the "
    "provided context. If the answer cannot be determined from the context, "
    "say so explicitly. Do not fabricate information. "
    "Keep answers concise and directly address the user's question."
)


def answer_with_context(
    question: str,
    context: str,
    model: Optional[str] = None,
    temperature: float = 0.3,
    max_tokens: Optional[int] = None,
) -> CompletionResponse:
    """
    Answer a question using provided context via the hosted OpenAI gpt-4o model.

    Parameters
    ----------
    question : str
        The question to answer.
    context : str
        Reference text the answer should be grounded in.
    model : str, optional
        Concrete OpenAI model ID (defaults to gpt-4o-2024-08-06).
    temperature : float
        Sampling temperature.
    max_tokens : int, optional
        Maximum output tokens.

    Returns
    -------
    CompletionResponse
        The answer along with token usage metadata.
    """
    target_model = model or QA_MODEL
    user_prompt = f"Context:\n{context}\n\nQuestion: {question}"
    request = build_chat_request(
        system_prompt=QA_SYSTEM_PROMPT,
        user_prompt=user_prompt,
        model=target_model,
        temperature=temperature,
        max_tokens=max_tokens,
    )
    return run_completion(request)


if __name__ == "__main__":
    ctx = (
        "The Apollo 11 mission launched on July 16, 1969, from Kennedy Space "
        "Center in Florida. The crew consisted of Commander Neil Armstrong, "
        "Command Module Pilot Michael Collins, and Lunar Module Pilot Buzz "
        "Aldrin. On July 20, 1969, Armstrong and Aldrin became the first humans "
        "to land on the Moon, while Collins remained in lunar orbit."
    )
    q = "Who remained in lunar orbit during the Apollo 11 moon landing?"
    result = answer_with_context(q, ctx)
    print(f"Answer ({result.model}):\n{result.content}")
