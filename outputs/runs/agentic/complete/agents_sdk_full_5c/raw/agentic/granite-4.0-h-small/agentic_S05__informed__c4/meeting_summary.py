# [LATER-STEP] meeting_summary.py
# Summarize live meeting transcript chunks using Anthropic Claude 3 Sonnet model via its Messages endpoint
import asyncio
import json
import openai  # using openai SDK which works with Anthropic via alias

# Provider identifier
PROVIDER = "anthropic"

# Environment variables
ANTHROPIC_API_KEY = "${ANTHROPIC_API_KEY}"
SYSTEM_PROMPT = "You are an assistant that summarizes short meeting transcripts into concise bullet points."

async def summarize(chunk: str) -> str:
    """Send a transcript chunk to Anthropic and return a summary."""
    client = openai.OpenAI(api_key=ANTHROPIC_API_KEY)
    response = client.beta.chat.completions.create(
        model="claude-3-sonnet-20240229",
        messages=[{"role": "system", "content": SYSTEM_PROMPT},
                  {"role": "user", "content": chunk}],
        temperature=0.0,
        max_tokens=150
    )
    return response.choices[0].message.content.strip()

async def live_summary(caption_source: asyncio.Queue):
    """Consume live captions and output a summary after each chunk."""
    summary_parts = []
    async for caption in caption_source:
        summary = await summarize(caption)
        summary_parts.append(summary)
        print(f"[SUMMARY] {summary}")

if __name__ == "__main__":
    # Demo: simple producer feeding captions into a queue
    q = asyncio.Queue()
    async def producer():
        lines = [
            "First, let's review the agenda items.",
            "We need to finalize the budget for Q2."
        ]
        for l in lines:
            await q.put(l)
            await asyncio.sleep(1.0)
    producer_task = asyncio.create_task(producer())
    summary_task = asyncio.create_task(live_summary(q.get()))
    await asyncio.sleep(3.0)
    producer_task.cancel()
    try:
        await producer_task
    except asyncio.CancelledError:
        pass