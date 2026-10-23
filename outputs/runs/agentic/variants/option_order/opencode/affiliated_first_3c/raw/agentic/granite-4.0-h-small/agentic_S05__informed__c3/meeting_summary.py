# Mistral Chat API (service=Mistral Chat API; sdk=mistralai)
# MISTRAL_API_KEY environment variable required

import os
import asyncio
import mistralai
from .speech_models import normalize_result

MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
if not MISTRAL_API_KEY:
    raise RuntimeError("Missing MISTRAL_API_KEY")

client = mistralai.ChatClient(api_key=MISTRAL_API_KEY)


async def summarize(transcript_chunks):
    """Summarize meeting transcript chunks using Mistral."""
    system_prompt = "You are a professional meeting summarizer. Produce a concise bullet‑point summary of the discussion."
    assistant_response = ""
    async for chunk in transcript_chunks:
        # Append new chunk to conversation history
        response = await client.chat(
            system=system_prompt,
            messages=[{"role": "user", "content": chunk}],
            max_tokens=200,
        )
        # Append assistant reply to history for next chunk
        assistant_response += response.choices[0].message.content + "\n"
        # Output partial summary after each chunk
        print("Current summary:", assistant_response)


async def demo():
    demo_lines = [
        "Welcome everyone to the product roadmap meeting.",
        "We discussed the upcoming feature releases for Q4.",
        "Key points: new dashboard, API improvements, and beta testing.",
    ]

    async def gen():
        for line in demo_lines:
            yield line
            await asyncio.sleep(0.1)

    await summarize(gen())


if __name__ == "__main__":
    asyncio.run(demo())
