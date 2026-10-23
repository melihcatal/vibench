import os
from openai import OpenAI
from model_client import get_client
from model_models import SummaryRequest, SummaryResponse


def summarize_text(text: str, max_length: int = 200) -> str:
    """
    Summarize long text using a hosted LLM.

    Args:
        text: The text to summarize
        max_length: Maximum length of the summary

    Returns:
        The summarized text
    """
    client = get_client()

    prompt = f"""Please summarize the following text in {max_length} words or less:

{text}

Summary:"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful text summarizer."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=max_length * 2,
            temperature=0.3,
        )

        summary = response.choices[0].message.content.strip()
        return summary

    except Exception as e:
        raise Exception(f"Failed to summarize text: {str(e)}")
