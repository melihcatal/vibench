# meeting_summary.py
# [LATER-STEP]
# Summarize live meeting transcript chunks using Anthropic Claude via the Claude messages API

import asyncio
import os
import sys
import openai  # also works for Anthropic with the right key handling

# Load Anthropic API key from environment
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "${ANTHROPIC_API_KEY}")
openai.api_key = ANTHROPIC_API_KEY
# Set Anthropic model explicitly
openai.default_model = "claude-3-5-sonnet-20240620"

# Simple in-memory conversation store
conversation = []


async def add_chunk_to_conversation(chunk: str):
    """Append a new transcript chunk to the conversation history and optionally trim history."""
    conversation.append({"role": "user", "content": chunk})
    # Keep only the most recent ~5 messages to respect model context window (~100k tokens max)
    if len(conversation) > 10:
        conversation.pop(0)


async def get_meeting_summary():
    """Generate a concise summary of the accumulated conversation."""
    messages = [
        {
            "role": "system",
            "content": "You are an assistant that produces a concise, bullet-point summary of a meeting transcript. Only output the summary, no explanations.",
        }
    ]
    messages.extend(conversation)
    try:
        response = await openai.ChatCompletion.create(
            model=openai.default_model, messages=messages
        )
    except Exception as exc:
        print("Summary generation error:", exc)
        return ""
    # Anthropic returns completion.choices[0].message.content
    summary = response.choices[0].message.content.strip()
    return summary


async def run_live_summary(recognizer: deepgram.client.StreamingRecognizer):
    """Consume live captions, build conversation, and print periodic summaries."""
    captions = []
    async for caption in recognizer.interim_results():
        # Each caption is a dict; extract transcript safely
        text = extract_transcript(caption)
        if text:
            await add_chunk_to_conversation(text)
            # Summarize every ~30 seconds or when enough context is gathered
            if len(captions) % 10 == 0:
                summary = await get_meeting_summary()
                print("=== Meeting Summary ===\n", summary, "\n=== End Summary ===")
    # Final summary after stream ends
    final_summary = await get_meeting_summary()
    print(
        "=== Final Meeting Summary ===\n", final_summary, "\n=== End Final Summary ==="
    )


# Helper to extract transcript from Deepgram result dict


def extract_transcript(result: dict) -> str:
    try:
        return result["results"][0]["alternatives"][0]["transcript"]
    except (KeyError, IndexError, TypeError):
        return ""


if __name__ == "__main__":
    # Demo: read from a local WAV file (requires pyaudio & wav)
    import sys

    audio_path = sys.argv[1] if len(sys.argv) > 1 else "sample.wav"
    client = deepgram.client.Client(DEEPGRAM_API_KEY)
    recognizer = client.streaming_recognize(
        model="nvidia_large", language="en", punctuate=False, interim_results=True
    )
    asyncio.run(run_live_summary(recognizer))

# Export the summary functions for import elsewhere if needed
__all__ = ["add_chunk_to_conversation", "get_meeting_summary"]
