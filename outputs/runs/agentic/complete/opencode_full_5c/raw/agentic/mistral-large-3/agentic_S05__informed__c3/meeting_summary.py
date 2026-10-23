import os
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
from typing import AsyncIterable, List

client = MistralClient(api_key=os.getenv("MISTRAL_API_KEY"))


async def summarize_text(chunks: List[str]) -> str:
    """Summarizes meeting transcript chunks using Mistral's model."""
    prompt = (
        "Summarize the following meeting transcript chunks into a concise summary. "
        "Focus on key decisions, action items, and important discussions:\n\n"
    )
    prompt += "\n".join(chunks)

    response = client.chat(
        model="mistral-large-latest",
        messages=[ChatMessage(role="user", content=prompt)],
        temperature=0.3,
    )
    return response.choices[0].message.content.strip()


async def meeting_summary(transcript_chunks: AsyncIterable[List[str]]):
    """Summarizes live meeting transcript chunks."""
    async for chunks in transcript_chunks:
        summary = await summarize_text(chunks)
        yield summary
