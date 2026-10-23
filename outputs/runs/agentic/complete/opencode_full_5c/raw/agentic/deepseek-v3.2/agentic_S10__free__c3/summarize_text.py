import os
from typing import Optional
from openai import OpenAI
from model_client import get_llm_client
from model_models import SummaryRequest, SummaryResponse


def summarize_text(text: str, max_length: Optional[int] = None) -> SummaryResponse:
    """
    Summarize long text using a hosted LLM.

    Args:
        text: The text to summarize
        max_length: Optional maximum length for the summary

    Returns:
        SummaryResponse containing the summarized text
    """
    client = get_llm_client()

    prompt = f"Please summarize the following text concisely:\n\n{text}"
    if max_length:
        prompt += f"\n\nKeep the summary under {max_length} characters."

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that creates concise summaries.",
                },
                {"role": "user", "content": prompt},
            ],
            max_tokens=500,
            temperature=0.3,
        )

        summary = response.choices[0].message.content.strip()

        return SummaryResponse(
            original_text=text,
            summary=summary,
            model_used="gpt-4o-mini",
            provider="openai",
        )

    except Exception as e:
        raise Exception(f"Failed to summarize text: {str(e)}")
