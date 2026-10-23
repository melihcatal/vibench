# archive_summary.py
import os
from typing import Dict, Any, List

# Use DashScope Qwen model for summarizing transcription results
from dashscope import text  # type: ignore

# Load configuration from environment variables
DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY")


def archive_summary(
    transcript_segments: List[str], max_words: int = 200
) -> Dict[str, Any]:
    """Generates a concise summary of transcription segments.

    Uses the DashScope Qwen API as the concrete provider.
    Returns a dictionary containing the original transcript list and the generated summary.
    """
    client = text.Client(api_key=DASHSCOPE_API_KEY)
    # Concatenate segments for summarization (optional: could summarize each separately)
    full_text = " \n".join(transcript_segments)
    response = client.chat_completion(
        system_prompt="You are a summarizer. Provide a concise summary of the input, up to MAX_WORDS words.",
        messages=[{"role": "user", "content": full_text}],
        max_tokens=max_words,
    )
    summary = response["choices"][0]["message"]["content"]
    return {
        "original_segments": transcript_segments,
        "summary": summary.strip(),
    }
