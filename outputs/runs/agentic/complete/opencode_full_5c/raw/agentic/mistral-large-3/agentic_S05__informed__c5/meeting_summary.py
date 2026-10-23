import os
from typing import AsyncGenerator, Dict, Any, List
from anthropic import AsyncAnthropic


async def meeting_summary(
    transcript_chunks: AsyncGenerator[List[Dict[str, Any]], None],
) -> AsyncGenerator[Dict[str, Any], None]:
    """Summarizes live meeting transcript chunks using Anthropic's Claude model."""
    client = AsyncAnthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    async for chunk in transcript_chunks:
        texts = [item["transcript"] for item in chunk if item["is_final"]]
        if not texts:
            continue

        response = await client.messages.create(
            model="claude-3-5-sonnet-20240620",
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": f"Summarize the following meeting transcript:\n\n{' '.join(texts)}",
                }
            ],
        )
        summary = response.content[0].text.strip()
        yield {
            "summary": summary,
            "chunk_size": len(texts),
        }
