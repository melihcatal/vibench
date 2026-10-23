import os
import asyncio
from typing import Optional, List, Dict, Any

import anthropic

from speech_models import NormalizedTranscript


def load_anthropic_config(api_key: Optional[str] = None) -> dict:
    key = api_key or os.environ.get("ANTHROPIC_API_KEY")
    if not key:
        raise ValueError("ANTHROPIC_API_KEY environment variable is required")
    return {"api_key": key}


def create_anthropic_client(api_key: Optional[str] = None) -> anthropic.Anthropic:
    config = load_anthropic_config(api_key)
    return anthropic.Anthropic(api_key=config["api_key"])


MEETING_SUMMARY_PROMPT = """You are a meeting summarization assistant. Given a transcript of a meeting, provide a structured summary.

Return the summary in the following JSON format:
{
  "title": "Meeting title",
  "key_points": ["point 1", "point 2", ...],
  "action_items": [{"assignee": "name or TBD", "task": "description", "deadline": "if mentioned or TBD"}],
  "decisions": ["decision 1", "decision 2", ...],
  "open_questions": ["question 1", "question 2", ...]
}

Transcript:
{transcript}
"""


async def summarize_meeting_chunks(
    chunks: List[NormalizedTranscript],
    api_key: Optional[str] = None,
    model: str = "claude-3-5-sonnet-20241022",
    max_tokens: int = 2048,
) -> Dict[str, Any]:
    client = create_anthropic_client(api_key)

    transcript_text = " ".join(chunk.text for chunk in chunks if chunk.text.strip())

    if not transcript_text.strip():
        return {
            "title": "Empty Meeting",
            "key_points": [],
            "action_items": [],
            "decisions": [],
            "open_questions": [],
        }

    prompt = MEETING_SUMMARY_PROMPT.format(transcript=transcript_text)

    loop = asyncio.get_event_loop()

    def _call_anthropic():
        message = client.messages.create(
            model=model,
            max_tokens=max_tokens,
            system="You are a professional meeting summarization assistant. Always respond with valid JSON.",
            messages=[{"role": "user", "content": prompt}],
        )
        return message.content[0].text

    response_text = await loop.run_in_executor(None, _call_anthropic)

    import json

    try:
        start_idx = response_text.find("{")
        end_idx = response_text.rfind("}") + 1
        if start_idx >= 0 and end_idx > start_idx:
            summary = json.loads(response_text[start_idx:end_idx])
        else:
            summary = {
                "title": "Meeting Summary",
                "key_points": [response_text],
                "action_items": [],
                "decisions": [],
                "open_questions": [],
            }
    except json.JSONDecodeError:
        summary = {
            "title": "Meeting Summary",
            "key_points": [response_text],
            "action_items": [],
            "decisions": [],
            "open_questions": [],
        }

    return summary


async def summarize_live_meeting(
    caption_stream,
    api_key: Optional[str] = None,
    model: str = "claude-3-5-sonnet-20241022",
    chunk_size: int = 10,
    max_tokens: int = 2048,
):
    buffer: List[NormalizedTranscript] = []
    summary_count = 0

    async for caption in caption_stream:
        buffer.append(caption)
        if len(buffer) >= chunk_size:
            summary = await summarize_meeting_chunks(
                chunks=buffer,
                api_key=api_key,
                model=model,
                max_tokens=max_tokens,
            )
            summary_count += 1
            buffer = []
            yield {
                "summary_index": summary_count,
                "summary": summary,
                "chunks_processed": chunk_size,
            }

    if buffer:
        summary = await summarize_meeting_chunks(
            chunks=buffer,
            api_key=api_key,
            model=model,
            max_tokens=max_tokens,
        )
        summary_count += 1
        yield {
            "summary_index": summary_count,
            "summary": summary,
            "chunks_processed": len(buffer),
        }
