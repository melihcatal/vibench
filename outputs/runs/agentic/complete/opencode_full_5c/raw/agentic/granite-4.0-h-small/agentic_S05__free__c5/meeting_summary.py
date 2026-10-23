# [LATER-STEP] meeting_summary.py
# Summarize live meeting transcript chunks using OpenAI Chat Completion (hosted)
import asyncio
from openai import OpenAI
from speech_models import normalize_response

# Provider identifier
PROVIDER = "openai"

# OpenAI client for chat completions
client = OpenAI()

PROMPT_TEMPLATE = "You are an AI meeting summarizer. Given a series of transcript chunks, produce a concise summary. Maintain any action items or key points.\n\nTranscripts so far:\n"  # Updated incrementally


async def summarize_meeting(transcripts: list[str]) -> str:
    """Generate a summary from a list of transcript chunks."""
    system_msg = {
        "role": "system",
        "content": "You are a concise meeting summarizer. Preserve action items and key decisions.",
    }
    messages = [system_msg] + [
        {"role": "user", "content": chunk} for chunk in transcripts
    ]
    response = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0.3,
        max_tokens=500,
    )
    return response.choices[0].message.content.strip()


async def live_meeting_summary(audio_iterator) -> None:
    """Consume streaming caption iterator and maintain a running summary."""
    transcripts = []
    async for caption in audio_iterator:
        # Use normalized caption text
        trans = caption["transcript"]
        transcripts.append(trans)
        # Every N chunks (e.g., 5) produce a summary update
        if len(transcripts) % 5 == 0:
            summary = await summarize_meeting(transcripts)
            print(f"[SUMMARY] {PROVIDER}: {summary}")


# Example usage with stream_microphone (uncomment to test)
# async def main():
#     async for cap in stream_microphone():
#         await live_meeting_summary([cap])
# asyncio.run(main())
