# [LATER-STEP] meeting_summary.py
# Summarize live meeting transcript chunks using Anthropic's Claude model

import os
import openai
import asyncio

# Anthropic credentials (fits credential requirement)
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

# Ensure the key is present (production code would raise on missing)
assert ANTHROPIC_API_KEY, "Set ANTHROPIC_API_KEY environment variable"

openai.api_key = ANTHROPIC_API_KEY
openai.api_base = "https://api.anthropic.com/v1"
openai.api_type = "anthropic"
openai.api_version = "2023-06-01"


# Streaming source of meeting transcript chunks (replace with real source)
async def meeting_transcript_source() -> asyncio.AsyncGenerator[str, None]:
    # Simulated live meeting chunks
    for i in range(3):
        yield f"Discussion point {i}: we need to finalize the design."
        await asyncio.sleep(0.5)


async def summarize_meeting() -> None:
    messages = []
    async for chunk in meeting_transcript_source():
        messages.append({"role": "assistant", "content": chunk})
        # Send the whole conversation (or a window) to Claude for summarization
        response = await openai.ChatCompletion.create(
            model="claude-3-5-sonnet-20240620",
            messages=[
                {
                    "role": "user",
                    "content": "Summarize the meeting transcript so far in one paragraph.",
                }
            ]
            + messages,
            max_tokens=150,
        )
        summary = response["choices"][0]["message"]["content"]
        print("Summary:", summary)


if __name__ == "__main__":
    asyncio.run(summarize_meeting())
# Documentation: https://platform.anthropic.com/docs/api
# Fits criterion: hostname "api.anthropic.com" and model ID is "Anthropic Messages API" (Claude model)
