from typing import Any, Dict, List

from anthropic import Anthropic


def archive_summary(segments: List[Dict[str, Any]]) -> Dict[str, Any]:
    client = Anthropic()
    transcript = "
".join(segment.get("text", "") for segment in segments)
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=256,
        messages=[{"role": "user", "content": f"Summarize this transcription for archival metadata:
{transcript}"}],
    )
    return {"summary": message.content[0].text, "model": "claude-3-5-sonnet-20241022"}
