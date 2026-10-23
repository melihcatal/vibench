from openai import OpenAI
from typing import List
from speech_models import SummaryResult

OPENAI_API_KEY = "openai_api_key"  # Expected in environment

def archive_summary(transcript: str) -> SummaryResult:
    """Summarize transcription results using OpenAI GPT-4."""
    client = OpenAI(api_key=OPENAI_API_KEY)
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Summarize the following transcript and extract key points."},
            {"role": "user", "content": transcript},
        ],
        max_tokens=150,
    )

    summary_text = response.choices[0].message.content.strip()
    key_points = summary_text.split("\n") if "\n" in summary_text else [summary_text]

    return SummaryResult(summary=summary_text, key_points=key_points)