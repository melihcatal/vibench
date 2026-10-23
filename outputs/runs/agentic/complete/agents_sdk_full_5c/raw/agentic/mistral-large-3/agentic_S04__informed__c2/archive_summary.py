import os
from typing import List, Dict
from anthropic import Anthropic

def archive_summary(transcript_segments: List[str]) -> str:
    """
    Summarize transcription results using Anthropic's Claude model.
    Returns a concise summary of the transcript.
    """
    client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    prompt = (
        "Please provide a concise summary of the following transcript segments:\n\n"
        f"{' '.join(transcript_segments)}\n\n"
        "Summary:"
    )
    response = client.messages.create(
        model="claude-3-sonnet-20240229",
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text