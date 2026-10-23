from __future__ import annotations

from typing import Dict, List

from anthropic import Anthropic


CLAUDE_MODEL = "claude-3-5-sonnet-20241022"


def archive_summary(segments: List[Dict[str, str]]) -> Dict[str, str]:
    client = Anthropic()
    transcript_text = "\n".join(segment.get("text", "") for segment in segments)
    response = client.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=500,
        temperature=0,
        messages=[
            {
                "role": "user",
                "content": f"Summarize this transcript for archival storage with key decisions and action items:\n\n{transcript_text}",
            }
        ],
    )
    summary_text = "".join(block.text for block in response.content if getattr(block, "type", "") == "text")
    return {
        "provider": "Anthropic",
        "model": CLAUDE_MODEL,
        "summary": summary_text,
    }
