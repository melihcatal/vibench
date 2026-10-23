import asyncio
import os
from typing import AsyncGenerator, AsyncIterator
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage


class MeetingSummarizer:
    def __init__(self, client: MistralClient, model: str = "mistral-small-latest"):
        self.client = client
        self.model = model
        self.transcript = ""

    def add_chunk(self, chunk: str) -> bool:
        self.transcript += " " + chunk
        return len(self.transcript) > 3000

    def get_summary(self) -> str:
        if len(self.transcript.strip()) == 0:
            return ""
        messages = [
            {
                "role": "system",
                "content": "Summarize the meeting discussion in concise bullet points, focusing on key decisions, action items, and topics.",
            },
            {"role": "user", "content": self.transcript},
        ]
        response = self.client.chat(model=self.model, messages=messages)
        summary = response.choices[0].message.content
        self.transcript = summary + "\n"  # chain
        return summary


async def summarize_live_meeting(
    chunks: AsyncIterator[str],
) -> AsyncGenerator[str, None]:
    api_key = os.getenv("MISTRAL_API_KEY")
    if not api_key:
        raise ValueError("MISTRAL_API_KEY required")
    client = MistralClient(api_key=api_key)
    summarizer = MeetingSummarizer(client)
    loop = asyncio.get_event_loop()
    async for chunk in chunks:
        if summarizer.add_chunk(chunk):
            summary = await loop.run_in_executor(None, summarizer.get_summary)
            if summary:
                yield summary
