# LATER-STEP: archive_summary.py

# Summarize a completed transcription using Anthropic Claude (via API)
# Provider: Anthropic (ANTHROPIC_API_KEY environment variable)
import os
import openai  # Using OpenAI's client as a drop‑in for Anthropic's chat completions endpoint

openai.api_key = os.getenv("ANTHROPIC_API_KEY")
if not openai.api_key:
    raise RuntimeError("ANTHROPIC_API_KEY environment variable not set")


def summarize_transcript(transcript: str, max_tokens: int = 150) -> str:
    """Generate a concise summary of a full transcript."""
    response = openai.ChatCompletion.create(
        model="anthropic.claude-3-sonnet-20240229",
        messages=[{"role": "user", "content": transcript}],
        temperature=0.0,
        max_tokens=max_tokens,
    )
    return response.choices[0].message.content.strip()
