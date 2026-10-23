"""
Call a hosted LLM (OpenAI gpt-4o) to summarize long text.

Uses OpenAI platform API at api.openai.com with concrete model gpt-4o.
"""

from typing import Optional

from model_client import (
    create_openai_client,
    execute_chat_completion,
    select_model_for_task,
)
from model_models import LLMRequest, build_system_prompt, build_completion_prompt


def summarize_text(
    text: str,
    length: str = "medium",
    model: Optional[str] = None,
    temperature: float = 0.5,
    max_tokens: int = 1024,
) -> str:
    """Summarize long text using OpenAI's hosted LLM.

    Args:
        text: The text to summarize.
        length: Desired summary length ('short', 'medium', 'long').
        model: Specific OpenAI model to use (defaults to gpt-4o).
        temperature: Sampling temperature.
        max_tokens: Maximum tokens in the output.

    Returns:
        The summarized text string.
    """
    if model is None:
        model = select_model_for_task("summarize", quality_preference="high")

    system_prompt = build_system_prompt("summarize", length=length)
    user_prompt = build_completion_prompt("summarize", text=text)

    request = LLMRequest(
        model=model,
        prompt=user_prompt,
        system_prompt=system_prompt,
        temperature=temperature,
        max_tokens=max_tokens,
    )

    response = execute_chat_completion(request)
    return response.text


def summarize_with_options(
    text: str,
    style: str = "bullet_points",
    focus_areas: Optional[list] = None,
    model: Optional[str] = None,
) -> str:
    """Summarize with additional style and focus options.

    Args:
        text: The text to summarize.
        style: Summary style ('paragraph', 'bullet_points', 'executive').
        focus_areas: List of topics or sections to focus on.
        model: OpenAI model identifier.

    Returns:
        The formatted summary.
    """
    if model is None:
        model = "gpt-4o"

    style_instructions = {
        "bullet_points": "Use bullet points for each key finding.",
        "executive": "Provide a brief executive summary suitable for leadership.",
        "paragraph": "Write in cohesive paragraphs.",
    }

    focus_text = ""
    if focus_areas:
        focus_text = f"\nPay special attention to these areas: {', '.join(focus_areas)}"

    system_prompt = (
        f"You are an expert summarizer. {style_instructions.get(style, '')}"
        f"Maintain factual accuracy.{focus_text}"
    )

    request = LLMRequest(
        model=model,
        prompt=f"Summarize this text:\n\n{text}",
        system_prompt=system_prompt,
        temperature=0.5,
        max_tokens=1500,
    )

    response = execute_chat_completion(request)
    return response.text


if __name__ == "__main__":
    sample_text = (
        "Machine learning is a subset of artificial intelligence that focuses on "
        "building systems that learn from data. Rather than explicitly programming "
        "rules, ML algorithms identify patterns and make decisions with minimal "
        "human intervention. Deep learning, a further subset, uses neural networks "
        "with many layers to analyze data. Applications range from natural language "
        "processing to computer vision and autonomous systems."
    )
    result = summarize_text(sample_text, length="short")
    print(result)
