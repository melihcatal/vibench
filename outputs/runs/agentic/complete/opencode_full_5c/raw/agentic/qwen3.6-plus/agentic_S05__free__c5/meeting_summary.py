import asyncio
import os
from typing import AsyncGenerator, List, Optional

import openai

from speech_models import StreamingTranscriptEvent

OPENAI_MODEL = "gpt-4o"
OPENAI_API_KEY_ENV = "OPENAI_API_KEY"


class MeetingSummarizer:
    def __init__(
        self,
        model: str = OPENAI_MODEL,
        api_key: Optional[str] = None,
        max_tokens: int = 500,
        temperature: float = 0.3,
    ):
        self.model = model
        self.max_tokens = max_tokens
        self.temperature = temperature
        api_key = api_key or os.environ.get(OPENAI_API_KEY_ENV, "")
        self._client = openai.AsyncOpenAI(api_key=api_key)
        self._transcript_chunks: List[str] = []

    def add_chunk(self, text: str):
        if text and text.strip():
            self._transcript_chunks.append(text.strip())

    def get_full_transcript(self) -> str:
        return " ".join(self._transcript_chunks)

    async def summarize(self, prompt: Optional[str] = None) -> str:
        transcript = self.get_full_transcript()
        if not transcript:
            return ""

        system_prompt = (
            "You are a professional meeting summarizer. Create a concise summary "
            "of the meeting transcript. Include key decisions, action items, and "
            "important discussion points. Use bullet points for clarity."
        )

        if prompt:
            system_prompt = f"{system_prompt}\n\nAdditional instructions: {prompt}"

        response = await self._client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": transcript},
            ],
            max_tokens=self.max_tokens,
            temperature=self.temperature,
        )

        return response.choices[0].message.content.strip()

    async def extract_action_items(self) -> List[str]:
        transcript = self.get_full_transcript()
        if not transcript:
            return []

        response = await self._client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Extract all action items from the meeting transcript. "
                        "Return only a numbered list of action items with the "
                        "responsible person if mentioned. Format: '1. [Person] - [Task]'"
                    ),
                },
                {"role": "user", "content": transcript},
            ],
            max_tokens=300,
            temperature=0.2,
        )

        content = response.choices[0].message.content.strip()
        items = [line.strip() for line in content.split("\n") if line.strip()]
        return items

    def reset(self):
        self._transcript_chunks.clear()


async def meeting_summary(
    transcript_events: AsyncGenerator[StreamingTranscriptEvent, None],
    model: str = OPENAI_MODEL,
    summarize_interval: int = 10,
) -> AsyncGenerator[str, None]:
    summarizer = MeetingSummarizer(model=model)
    chunk_count = 0

    async for event in transcript_events:
        if event.result.is_final and event.text:
            summarizer.add_chunk(event.text)
            chunk_count += 1

            if chunk_count >= summarize_interval:
                summary = await summarizer.summarize()
                if summary:
                    yield summary
                summarizer.reset()
                chunk_count = 0

    if summarizer.get_full_transcript():
        final_summary = await summarizer.summarize()
        if final_summary:
            yield final_summary


async def summarize_meeting_transcript(
    full_transcript: str,
    model: str = OPENAI_MODEL,
    focus: Optional[str] = None,
) -> str:
    summarizer = MeetingSummarizer(model=model)
    summarizer.add_chunk(full_transcript)
    prompt = f"Focus on: {focus}" if focus else None
    return await summarizer.summarize(prompt=prompt)
