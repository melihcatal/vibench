from __future__ import annotations

from typing import Optional

from model_client import call_llm
from model_models import LLMRequest, LLMResponse, normalize_prompt

SUMMARIZER_MODEL = "gpt-4o"
SUMMARIZER_SYSTEM_PROMPT = (
    "You are an expert summarizer. Provide a concise, accurate summary of the text provided. "
    "Preserve key facts, figures, and conclusions. Do not add information not present in the source."
)


def summarize_text(
    text: str,
    max_summary_length: int = 500,
    temperature: float = 0.3,
    model: Optional[str] = None,
    api_key: Optional[str] = None,
    base_url: Optional[str] = None,
) -> LLMResponse:
    normalized = normalize_prompt(text)
    prompt = (
        f"Summarize the following text in approximately {max_summary_length} words or fewer:\n\n"
        f"{normalized}"
    )
    request = LLMRequest(
        model=model or SUMMARIZER_MODEL,
        prompt=prompt,
        system_prompt=SUMMARIZER_SYSTEM_PROMPT,
        temperature=temperature,
        max_tokens=max_summary_length * 2,
    )
    return call_llm(request, api_key=api_key, base_url=base_url)


if __name__ == "__main__":
    import os

    response = summarize_text(
        text="Artificial intelligence has transformed industries worldwide...",
        api_key=os.environ.get("OPENAI_API_KEY"),
    )
    print(response.text)
