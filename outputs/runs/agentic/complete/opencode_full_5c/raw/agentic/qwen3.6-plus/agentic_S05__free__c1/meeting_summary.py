import os
from typing import AsyncIterator
from datetime import datetime

from vertexai.generative_models import GenerativeModel, GenerationConfig

from speech_models import StreamingResult, StreamingEvent


class MeetingSummarizer:
    def __init__(
        self,
        model_name: str = "gemini-1.5-pro-002",
        project_id: str | None = None,
        location: str = "us-central1",
        max_chunk_tokens: int = 4000,
    ):
        self.project_id = project_id or os.getenv("GOOGLE_CLOUD_PROJECT", "")
        self.location = location
        self.model_name = model_name
        self.max_chunk_tokens = max_chunk_tokens
        self._transcript_buffer: list[str] = []
        self._summaries: list[str] = []

        import vertexai

        vertexai.init(project=self.project_id, location=self.location)
        self._model = GenerativeModel(self.model_name)

    def add_transcript(self, text: str) -> None:
        if text.strip():
            self._transcript_buffer.append(text.strip())

    def _build_prompt(self) -> str:
        transcript = " ".join(self._transcript_buffer)
        return (
            f"You are a professional meeting summarizer. Summarize the following meeting transcript "
            f"concisely. Include key decisions, action items, and important discussion points.\n\n"
            f"Meeting Transcript:\n{transcript}\n\n"
            f"Summary:"
        )

    async def generate_summary(self) -> str:
        if not self._transcript_buffer:
            return ""

        prompt = self._build_prompt()
        response = self._model.generate_content(
            prompt,
            generation_config=GenerationConfig(
                max_output_tokens=1024,
                temperature=0.3,
                top_p=0.95,
            ),
        )
        summary = response.text.strip()
        self._summaries.append(summary)
        self._transcript_buffer.clear()
        return summary

    async def generate_incremental_summary(self, new_text: str) -> str:
        self.add_transcript(new_text)
        return await self.generate_summary()


async def meeting_summary(
    transcript_events: AsyncIterator[StreamingEvent],
    model_name: str = "gemini-1.5-pro-002",
    project_id: str | None = None,
    location: str = "us-central1",
    summary_interval: int = 5,
) -> AsyncIterator[dict]:
    summarizer = MeetingSummarizer(
        model_name=model_name,
        project_id=project_id,
        location=location,
    )
    event_count = 0
    async for event in transcript_events:
        if event.result and event.result.is_final:
            summarizer.add_transcript(event.result.transcript)
            event_count += 1

            if event_count % summary_interval == 0:
                summary = await summarizer.generate_summary()
                if summary:
                    yield {
                        "summary": summary,
                        "timestamp": datetime.utcnow().isoformat(),
                        "events_processed": event_count,
                    }

    final_summary = await summarizer.generate_summary()
    if final_summary:
        yield {
            "summary": final_summary,
            "timestamp": datetime.utcnow().isoformat(),
            "events_processed": event_count,
            "is_final": True,
        }
