"""
summarize_text.py — calls a hosted LLM (OpenAI gpt-4o) to summarize long text.

Uses the OpenAI Chat Completions API (api.openai.com) with the
gpt-4o-2024-08-06 model to produce concise summaries.
"""

from __future__ import annotations

from typing import Optional

from model_client import run_completion, resolve_model
from model_models import build_chat_request, CompletionResponse

# Concrete OpenAI model identifier for summarization
SUMMARIZATION_MODEL = resolve_model("gpt-4o")  # gpt-4o-2024-08-06

SUMMARIZATION_SYSTEM_PROMPT = (
    "You are an expert summarization assistant. "
    "Provide a clear, concise summary of the text provided by the user. "
    "Preserve key facts, names, and figures. "
    "Keep the summary between 3 and 5 sentences unless the user specifies otherwise."
)


def summarize_text(
    text: str,
    model: Optional[str] = None,
    temperature: float = 0.5,
    max_tokens: Optional[int] = None,
) -> CompletionResponse:
    """
    Summarize a long text using the hosted OpenAI gpt-4o model.

    Parameters
    ----------
    text : str
        The long-form text to summarize.
    model : str, optional
        Concrete OpenAI model ID to use (defaults to gpt-4o-2024-08-06).
    temperature : float
        Sampling temperature.
    max_tokens : int, optional
        Maximum output tokens.

    Returns
    -------
    CompletionResponse
        The summary along with token usage metadata.
    """
    target_model = model or SUMMARIZATION_MODEL
    request = build_chat_request(
        system_prompt=SUMMARIZATION_SYSTEM_PROMPT,
        user_prompt=text,
        model=target_model,
        temperature=temperature,
        max_tokens=max_tokens,
    )
    return run_completion(request)


if __name__ == "__main__":
    sample_text = (
        "The Industrial Revolution began in Great Britain in the late 18th century "
        "and quickly spread to continental Europe and North America. It was characterized "
        "by the transition from hand production methods to machines, new chemical and iron "
        "manufacturing processes, the increasing use of steam power and water power, and the "
        "development of machine tools. These changes led to unprecedented population growth "
        "and urbanization, fundamentally altering social and economic structures worldwide."
    )
    result = summarize_text(sample_text)
    print(f"Summary ({result.model}):\n{result.content}")
    print(f"Tokens: {result.total_tokens}")
