"""
Calls a hosted LLM (OpenAI GPT-4o) to summarize long text.

Provider: OpenAI (api.openai.com)
Model family: gpt-4o
"""

from typing import Optional

from model_client import (
    get_sync_client,
    select_model_family,
    build_system_message,
    build_user_message,
    configure_completion_kwargs,
)
from model_models import (
    SummarizeRequest,
    SummarizeResponse,
    extract_text_from_openai_response,
    extract_token_usage,
)

OPENAI_API_HOST = "api.openai.com"
OPENAI_MODEL_FAMILY = "gpt-4o"


def build_summarize_instruction(request: SummarizeRequest) -> str:
    """Build the system instruction for summarization."""
    return (
        f"You are an expert text summarizer using OpenAI's {OPENAI_MODEL_FAMILY} model family. "
        f"Summarize the provided text in a {request.style} style. "
        f"Keep the summary to approximately {request.max_summary_length} words or fewer. "
        f"Preserve key facts, names, and numbers."
    )


def summarize_text(
    request: SummarizeRequest,
    model: Optional[str] = None,
    temperature: float = 0.3,
) -> SummarizeResponse:
    """
    Summarize long text using OpenAI GPT-4o hosted LLM.

    Args:
        request: SummarizeRequest with text and parameters.
        model: Optional explicit OpenAI model identifier (defaults to gpt-4o family).
        temperature: Sampling temperature for generation.

    Returns:
        SummarizeResponse containing the summary text and metadata.
    """
    selected_model = model or select_model_family("summarize")

    system_msg = build_system_message(build_summarize_instruction(request))
    user_msg = build_user_message(request.text)

    client = get_sync_client()

    kwargs = configure_completion_kwargs(
        messages=[system_msg, user_msg],
        model=selected_model,
        temperature=temperature,
        max_tokens=2048,
    )

    completion = client.chat.completions.create(**kwargs)

    summary = extract_text_from_openai_response(completion)
    usage = extract_token_usage(completion)

    return SummarizeResponse(
        summary=summary,
        model_used=selected_model,
        token_usage=usage,
    )


if __name__ == "__main__":
    sample = SummarizeRequest(
        text="Provide your long text here to summarize.",
        max_summary_length=150,
        style="concise",
    )
    result = summarize_text(sample)
    print(f"Model: {result.model_used}")
    print(f"Summary: {result.summary}")
