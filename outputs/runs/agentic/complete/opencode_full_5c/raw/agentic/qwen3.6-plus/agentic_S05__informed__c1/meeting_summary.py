import os
from typing import Optional, List
from dataclasses import dataclass

from anthropic import Anthropic

from speech_models import StreamingRecognitionResult, normalize_transcript_text


ANTHROPIC_MODEL = "claude-3-sonnet-20240229"
ANTHROPIC_API_HOST = "api.anthropic.com"

DEFAULT_SUMMARY_PROMPT = """You are a meeting assistant. Summarize the following meeting transcript.
Provide:
1. A brief overview of what was discussed
2. Key decisions made
3. Action items with owners if mentioned
4. Open questions or topics for follow-up

Keep the summary concise and structured."""

DEFAULT_MAX_TOKENS = 1024


@dataclass
class MeetingSummary:
    transcript_chunks: List[str]
    summary_text: str
    model_used: str
    token_usage: Optional[dict] = None


def load_anthropic_api_key() -> str:
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise EnvironmentError(
            "ANTHROPIC_API_KEY environment variable is required for Anthropic Messages API"
        )
    return api_key


def create_anthropic_client(api_key: Optional[str] = None) -> Anthropic:
    key = api_key or load_anthropic_api_key()
    return Anthropic(api_key=key)


def build_meeting_context(
    transcript_chunks: List[str],
    max_chunks: Optional[int] = None,
) -> str:
    chunks = transcript_chunks[-max_chunks:] if max_chunks else transcript_chunks
    context_parts = []
    for i, chunk in enumerate(chunks, 1):
        context_parts.append(f"[Segment {i}]: {chunk}")
    return "\n\n".join(context_parts)


async def summarize_meeting(
    transcript_chunks: List[str],
    client: Optional[Anthropic] = None,
    model: str = ANTHROPIC_MODEL,
    system_prompt: Optional[str] = None,
    max_tokens: int = DEFAULT_MAX_TOKENS,
    temperature: float = 0.3,
    max_chunks: Optional[int] = None,
) -> MeetingSummary:
    if client is None:
        client = create_anthropic_client()

    context = build_meeting_context(transcript_chunks, max_chunks=max_chunks)
    prompt = system_prompt or DEFAULT_SUMMARY_PROMPT

    message = f"{prompt}\n\n--- Transcript ---\n\n{context}"

    response = client.messages.create(
        model=model,
        max_tokens=max_tokens,
        temperature=temperature,
        messages=[{"role": "user", "content": message}],
    )

    summary_text = ""
    for block in response.content:
        if block.type == "text":
            summary_text += block.text

    token_usage = {
        "input_tokens": response.usage.input_tokens,
        "output_tokens": response.usage.output_tokens,
    }

    return MeetingSummary(
        transcript_chunks=transcript_chunks,
        summary_text=summary_text,
        model_used=model,
        token_usage=token_usage,
    )


async def summarize_live_transcript_stream(
    caption_stream,
    client: Optional[Anthropic] = None,
    model: str = ANTHROPIC_MODEL,
    chunk_window: int = 20,
    system_prompt: Optional[str] = None,
) -> MeetingSummary:
    buffer: List[str] = []

    async for caption in caption_stream:
        if caption.is_final and caption.text.strip():
            normalized = normalize_transcript_text(caption)
            buffer.append(normalized)

    return await summarize_meeting(
        transcript_chunks=buffer,
        client=client,
        model=model,
        system_prompt=system_prompt,
        max_chunks=chunk_window,
    )


async def generate_action_items(
    transcript_chunks: List[str],
    client: Optional[Anthropic] = None,
    model: str = ANTHROPIC_MODEL,
) -> str:
    if client is None:
        client = create_anthropic_client()

    context = build_meeting_context(transcript_chunks)

    prompt = f"""Extract all action items from the following meeting transcript.
For each action item, identify:
- The task description
- The person responsible (if mentioned)
- Any deadline mentioned (if any)

Format as a numbered list.

--- Transcript ---

{context}"""

    response = client.messages.create(
        model=model,
        max_tokens=512,
        temperature=0.2,
        messages=[{"role": "user", "content": prompt}],
    )

    result = ""
    for block in response.content:
        if block.type == "text":
            result += block.text
    return result
