import os
from typing import List
import openai


def archive_summary(segments: List[str]) -> str:
    """Generate a concise summary of transcript segments using OpenAI's GPT model.

    Args:
        segments: List of text chunks from a completed transcript.

    Returns:
        A short summary string.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("Missing OPENAI_API_KEY environment variable")

    prompt = (
        "You are a helpful AI assistant. Summarize the following transcript segments into a brief paragraph, preserving key points and overall tone.\n\n"
        + "\n\n".join(segments)
        + "\n\n"
    )
    resp = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a concise summarizer."},
            {"role": "user", "content": prompt},
        ],
    )
    return resp.choices[0].message.content.strip()
