# LATER-STEP: meeting_summary.py
# Summarize live meeting transcript chunks

import asyncio
import json
from openai import OpenAI  # pip install openai
from speech_models import TranscriptionResult, normalize_message

# OpenAI API client (single instance)
openai_client = OpenAI(api_key="YOUR_OPENAI_API_KEY")

SUMMARY_PROMPT = "Summarize the meeting discussion in 2-3 bullet points, focusing on decisions and action items."


async def summarize_live_meeting(stream_source: str, provider: str = "deepgram"):
    """Stream audio, transcribe in real time, and periodically produce a summary.

    Args:
        stream_source: Audio source URL or path (WebSocket endpoint, file, etc.).
        provider: Speech‑to‑Text provider ("deepgram", "google", "openai", etc.).
    """
    # Buffer to accumulate recent transcript fragments
    recent_transcript = []
    # Simple window: summarize after 5 final chunks
    summary_interval = 5
    chunk_counter = 0

    async for result in _simulate_stream_provider(provider, stream_source):
        if result.is_final:
            recent_transcript.append(result.text)
            chunk_counter += 1
            # When we have enough chunks, generate a summary
            if chunk_counter >= summary_interval:
                text_to_summarize = " ".join(recent_transcript)
                summary = await _generate_summary(text_to_summarize)
                print("[SUMMARY]", summary)
                # Reset buffer for next window (optional)
                recent_transcript = []
                chunk_counter = 0


async def _generate_summary(full_text: str) -> str:
    """Call OpenAI Chat Completion to produce a meeting summary."""
    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a concise meeting summarizer."},
            {
                "role": "user",
                "content": SUMMARY_PROMPT + "\n\nMeeting transcript:\n" + full_text,
            },
        ],
    )
    return response.choices[0].message.content.strip()


async def _simulate_stream_provider(
    provider: str, source: str
) -> AsyncGenerator[TranscriptionResult, None]:
    """Placeholder async generator mimicking live streaming.
    Replace with real streaming code from stream_microphone.py etc.
    """
    dummy_chunks = [
        TranscriptionResult(
            text="Welcome everyone to the product planning meeting.", is_final=True
        ),
        TranscriptionResult(
            text="We need to decide on the UI color scheme by Friday.", is_final=True
        ),
        TranscriptionResult(
            text="Action item: Alice will create the mockups.", is_final=True
        ),
        TranscriptionResult(
            text="Bob will write the spec doc by next Monday.", is_final=True
        ),
        TranscriptionResult(text="Any other items? The floor is open.", is_final=True),
    ]
    for chunk in dummy_chunks:
        yield chunk


if __name__ == "__main__":
    # Example: using Deepgram streaming (replace URL with real endpoint)
    asyncio.run(summarize_live_meeting("wss://example.com/stream", provider="deepgram"))
