from __future__ import annotations

from typing import Optional

from model_client import create_completion
from model_models import LLMRequest, normalize_messages


def summarize_text(
    text: str,
    max_length: Optional[int] = None,
    model: str = "gpt-4o-2024-08-06",
    temperature: float = 0.5,
) -> str:
    system_prompt = (
        "You are a concise summarization assistant. "
        "Provide a clear, accurate summary of the text provided. "
        "Focus on the main points and key takeaways."
    )
    if max_length:
        system_prompt += f" Keep the summary under {max_length} words."

    user_prompt = f"Please summarize the following text:\n\n{text}"
    messages = normalize_messages(system_prompt=system_prompt, user_prompt=user_prompt)

    request = LLMRequest(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=1024,
    )
    response = create_completion(request)
    return response.content


if __name__ == "__main__":
    import sys

    input_text = sys.stdin.read()
    result = summarize_text(input_text)
    print(result)
