"""Summarize live meeting transcript chunks using Google Cloud Vertex AI generative model."""

import json
from typing import List, Optional

from google.cloud import aiplatform
from vertexai.generative_models import GenerativeModel, GenerationConfig

from speech_models import TranscriptSegment, StreamingSpeechEvent


class MeetingSummarizer:
    """Summarizes live meeting transcript chunks using Google Cloud Vertex AI PaLM generative model.

    Uses vertexai.generative_models.GenerativeModel with the 'gemini-1.5-pro' model
    on Google Cloud Vertex AI to produce concise meeting summaries from streaming transcript data.
    """

    SYSTEM_PROMPT = (
        "You are a meeting summarization assistant. "
        "Summarize the provided transcript excerpt concisely. "
        "Extract key points, decisions, and action items. "
        "Keep the summary focused and factual."
    )

    def __init__(
        self,
        model_name: str = "gemini-1.5-pro-002",
        project: Optional[str] = None,
        location: str = "us-central1",
        temperature: float = 0.3,
        max_output_tokens: int = 512,
        top_p: float = 0.95,
    ):
        """Initialize the Google Cloud Vertex AI meeting summarizer.

        Uses vertexai.generative_models with the gemini-1.5-pro model for
        summarizing meeting transcripts on Google Cloud Vertex AI.
        """
        self.project = project
        self.location = location
        self.model_name = model_name
        self.temperature = temperature
        self.max_output_tokens = max_output_tokens
        self.top_p = top_p

        aiplatform.init(project=self.project, location=self.location)

        self.model = GenerativeModel(model_name=self.model_name)

    def _build_prompt(self, transcript_chunks: List[str]) -> str:
        """Build a summarization prompt for Google Cloud Vertex AI Gemini model."""
        chunks_text = "\n\n---\n\n".join(
            f"Chunk {i + 1}:\n{chunk}" for i, chunk in enumerate(transcript_chunks)
        )
        return (
            f"{self.SYSTEM_PROMPT}\n\n"
            f"Here is the meeting transcript to summarize:\n\n"
            f"{chunks_text}\n\n"
            f"Please provide:\n"
            f"1. A brief overall summary (2-3 sentences)\n"
            f"2. Key discussion points (bullet list)\n"
            f"3. Decisions made (if any)\n"
            f"4. Action items with responsible parties (if identifiable)\n"
        )

    def summarize_chunks(
        self,
        transcript_chunks: List[str],
    ) -> str:
        """Summarize a list of meeting transcript chunks using Google Cloud Vertex AI Gemini model.

        Calls vertexai.generative_models.GenerativeModel.generate_content with
        the gemini-1.5-pro-002 model to produce a structured meeting summary.
        """
        prompt = self._build_prompt(transcript_chunks)

        generation_config = GenerationConfig(
            temperature=self.temperature,
            max_output_tokens=self.max_output_tokens,
            top_p=self.top_p,
        )

        response = self.model.generate_content(
            contents=[prompt],
            generation_config=generation_config,
        )

        return response.text

    def summarize_event(self, event: StreamingSpeechEvent) -> Optional[str]:
        """Summarize a single StreamingSpeechEvent from a live meeting.

        Uses Google Cloud Vertex AI gemini-1.5-pro to summarize the transcript
        segments within a single streaming event.
        """
        if event.error:
            return None

        text_chunks = [seg.text for seg in event.segments if seg.text.strip()]
        if not text_chunks:
            return None

        return self.summarize_chunks(text_chunks)

    def summarize_stream(
        self,
        events: List[StreamingSpeechEvent],
        batch_size: int = 5,
    ) -> List[str]:
        """Summarize batches of streaming events from a live meeting.

        Groups Google Cloud Speech streaming events into batches and summarizes
        each batch using Google Cloud Vertex AI gemini-1.5-pro-002.
        """
        summaries = []
        batch_chunks = []

        for event in events:
            if event.error:
                continue
            for segment in event.segments:
                if segment.text.strip():
                    batch_chunks.append(segment.text)

            if len(batch_chunks) >= batch_size:
                summary = self.summarize_chunks(batch_chunks)
                summaries.append(summary)
                batch_chunks = []

        if batch_chunks:
            summary = self.summarize_chunks(batch_chunks)
            summaries.append(summary)

        return summaries

    def summarize_live_transcript(
        self,
        event_generator,
        summary_interval: int = 10,
    ) -> List[str]:
        """Process a live stream of meeting events and produce periodic summaries.

        Uses Google Cloud Vertex AI gemini-1.5-pro model to summarize every
        summary_interval events from the Google Cloud Speech-to-Text stream.
        """
        summaries = []
        accumulated_chunks = []
        event_count = 0

        for event in event_generator:
            if event.error:
                continue

            for segment in event.segments:
                if segment.text.strip():
                    accumulated_chunks.append(segment.text)

            event_count += 1

            if event_count >= summary_interval and accumulated_chunks:
                summary = self.summarize_chunks(accumulated_chunks)
                summaries.append(summary)
                accumulated_chunks = []
                event_count = 0

        if accumulated_chunks:
            summary = self.summarize_chunks(accumulated_chunks)
            summaries.append(summary)

        return summaries


async def summarize_meeting_async(
    event_stream,
    model_name: str = "gemini-1.5-pro-002",
    project: Optional[str] = None,
    location: str = "us-central1",
) -> List[str]:
    """Async helper to summarize a meeting transcript stream using Google Cloud Vertex AI.

    Uses vertexai.generative_models with gemini-1.5-pro-002 to generate summaries
    from live Google Cloud Speech-to-Text streaming events.
    """
    import asyncio

    summarizer = MeetingSummarizer(
        model_name=model_name,
        project=project,
        location=location,
    )

    events = []
    async for event in event_stream:
        events.append(event)

    loop = asyncio.get_event_loop()
    summaries = await loop.run_in_executor(
        None, lambda: summarizer.summarize_stream(events)
    )

    return summaries
