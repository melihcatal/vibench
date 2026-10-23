import os
from typing import List, Optional, Iterator
from google.cloud import aiplatform
from vertexai.generative_models import GenerativeModel
from vertexai.language_models import TextGenerationModel


class MeetingSummarizer:
    def __init__(
        self,
        model_name: str = "gemini-1.5-flash-002",
        temperature: float = 0.3,
        max_output_tokens: int = 1024,
    ):
        self.model_name = model_name
        self.temperature = temperature
        self.max_output_tokens = max_output_tokens
        self._transcript_chunks: List[str] = []
        self._initialized = False

    def initialize(self, project: Optional[str] = None, location: str = "us-central1"):
        if not self._initialized:
            aiplatform.init(
                project=project or os.environ.get("GOOGLE_CLOUD_PROJECT"),
                location=location,
            )
            self._initialized = True

    def add_chunk(self, transcript_chunk: str):
        if transcript_chunk.strip():
            self._transcript_chunks.append(transcript_chunk)

    def get_full_transcript(self) -> str:
        return " ".join(self._transcript_chunks)

    def summarize(self, summary_type: str = "comprehensive") -> str:
        self.initialize()
        model = GenerativeModel(self.model_name)

        full_transcript = self.get_full_transcript()
        if not full_transcript.strip():
            return ""

        if summary_type == "comprehensive":
            prompt = f"""Summarize the following meeting transcript comprehensively. Include:
- Key discussion points
- Decisions made
- Action items and owners
- Open questions

Transcript:
{full_transcript}

Summary:"""
        elif summary_type == "action_items":
            prompt = f"""Extract all action items from the following meeting transcript. Format as a list with owners and deadlines if mentioned.

Transcript:
{full_transcript}

Action Items:"""
        elif summary_type == "key_points":
            prompt = f"""Extract the key points from this meeting transcript as bullet points.

Transcript:
{full_transcript}

Key Points:"""
        else:
            prompt = f"""Provide a concise summary of this meeting transcript.

Transcript:
{full_transcript}

Summary:"""

        response = model.generate_content(
            prompt,
            generation_config={
                "temperature": self.temperature,
                "max_output_tokens": self.max_output_tokens,
            },
        )

        return response.text

    def summarize_chunks(self, chunk_size: int = 5) -> Iterator[str]:
        self.initialize()
        model = GenerativeModel(self.model_name)

        for i in range(0, len(self._transcript_chunks), chunk_size):
            batch = self._transcript_chunks[i : i + chunk_size]
            batch_text = " ".join(batch)

            if not batch_text.strip():
                continue

            prompt = f"""Summarize this portion of a meeting transcript concisely:

{batch_text}

Summary:"""

            response = model.generate_content(
                prompt,
                generation_config={
                    "temperature": self.temperature,
                    "max_output_tokens": 256,
                },
            )
            yield response.text

    def clear(self):
        self._transcript_chunks.clear()


def summarize_meeting(
    transcript: str,
    model_name: str = "gemini-1.5-flash-002",
    summary_type: str = "comprehensive",
    temperature: float = 0.3,
    max_output_tokens: int = 1024,
) -> str:
    summarizer = MeetingSummarizer(
        model_name=model_name,
        temperature=temperature,
        max_output_tokens=max_output_tokens,
    )
    summarizer.add_chunk(transcript)
    return summarizer.summarize(summary_type=summary_type)


def summarize_live_chunks(
    chunk_stream: Iterator[str],
    model_name: str = "gemini-1.5-flash-002",
    summarize_every: int = 5,
) -> Iterator[str]:
    summarizer = MeetingSummarizer(model_name=model_name)
    chunk_count = 0

    for chunk in chunk_stream:
        summarizer.add_chunk(chunk)
        chunk_count += 1

        if chunk_count % summarize_every == 0:
            yield summarizer.summarize(summary_type="key_points")
            summarizer.clear()

    if summarizer._transcript_chunks:
        yield summarizer.summarize(summary_type="key_points")
