"""Summarize transcription results using OpenAI GPT-4 via the OpenAI API.

Uses the openai SDK to call OpenAI's chat completions with the gpt-4o-mini model
for generating summaries of batch transcription outputs.
Auth: OPENAI_API_KEY environment variable.
"""

import os
from typing import List, Optional

from openai import OpenAI


def get_openai_client() -> OpenAI:
    """Create an OpenAI client using the OPENAI_API_KEY environment variable."""
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")
    return OpenAI(api_key=api_key)


def summarize_transcript(
    transcript: str,
    max_length: int = 500,
    style: str = "concise",
) -> str:
    """Generate a summary of a full transcript using OpenAI GPT-4o-mini.

    Args:
        transcript: The full transcription text to summarize.
        max_length: Maximum length of the summary in words.
        style: Summary style ('concise', 'detailed', 'bulleted').

    Returns:
        The summarized text.
    """
    client = get_openai_client()

    style_instructions = {
        "concise": "Provide a brief, one-paragraph summary.",
        "detailed": "Provide a thorough multi-paragraph summary capturing key points.",
        "bulleted": "Provide a summary as a bulleted list of key points.",
    }
    instruction = style_instructions.get(style, style_instructions["concise"])

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    f"You are a meeting transcription summarizer. {instruction} "
                    f"Keep the summary under {max_length} words. "
                    "Focus on actionable items, decisions, and key discussion points."
                ),
            },
            {
                "role": "user",
                "content": f"Here is the meeting transcript to summarize:\n\n{transcript}",
            },
        ],
        max_tokens=min(max_length * 2, 4096),
        temperature=0.3,
    )

    return response.choices[0].message.content or ""


def archive_summary(
    transcript: str,
    segments: Optional[List[str]] = None,
    job_id: str = "",
) -> dict:
    """Create a comprehensive archive summary of transcription results.

    Generates a summary and packages it with metadata for archival.

    Args:
        transcript: Full transcription text.
        segments: Optional list of segment strings for per-segment analysis.
        job_id: The transcription job identifier.

    Returns:
        Dict with summary, metadata, and archival info.
    """
    summary = summarize_transcript(transcript)

    # Generate per-segment key points for longer transcripts
    segment_key_points = []
    if segments and len(segments) <= 20:
        client = get_openai_client()
        for seg_text in segments:
            if len(seg_text) < 50:
                continue
            resp = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": "Extract the single most important point from this segment in one sentence.",
                    },
                    {
                        "role": "user",
                        "content": seg_text,
                    },
                ],
                max_tokens=60,
                temperature=0.2,
            )
            point = resp.choices[0].message.content or ""
            segment_key_points.append(point)

    return {
        "job_id": job_id,
        "summary": summary,
        "segment_key_points": segment_key_points,
        "word_count": len(transcript.split()),
        "num_segments": len(segments) if segments else 0,
    }


def main():
    import json
    import sys

    if len(sys.argv) > 1:
        with open(sys.argv[1], "r") as f:
            data = json.load(f)
        transcript = data.get("transcript", data.get("text", ""))
        segments = data.get("segments", None)
        job_id = data.get("job_id", "")
    else:
        transcript = """
        Welcome everyone to today's quarterly review meeting. 
        First, let's discuss our Q3 results. Revenue increased by 15% compared to last quarter.
        The engineering team successfully shipped the new API platform on schedule.
        Marketing reported a 25% increase in qualified leads from the new campaign.
        Action items: finalize Q4 budget by next Friday, schedule customer advisory board for November,
        and prepare the product roadmap presentation for the board meeting.
        Thank you all for your contributions. Let's reconvene next month.
        """
        segments = None
        job_id = "demo-job-001"

    result = archive_summary(transcript, segments=segments, job_id=job_id)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
