"""Summarize live meeting transcript chunks using Google Cloud Vertex AI.

Provider: Google Cloud Vertex AI (aiplatform.googleapis.com)
SDK: vertexai (google.cloud.aiplatform)
Model: text-bison / gemini-pro (Google's LLM for text summarization)
"""

from typing import Optional

import vertexai
from vertexai.preview.generative_models import GenerativeModel


VERTEX_AI_HOST = "aiplatform.googleapis.com"
VERTEX_AI_SUMMARY_MODEL = "gemini-1.0-pro-002"
VERTEX_AI_LOCATION = "us-central1"


def initialize_vertex_ai(
    project_id: Optional[str] = None,
    location: str = VERTEX_AI_LOCATION,
) -> None:
    """Initialize Vertex AI SDK.

    Provider: Google Cloud Vertex AI (aiplatform.googleapis.com)
    SDK: vertexai (google.cloud.aiplatform)
    """
    vertexai.init(project=project_id, location=location)


def get_summary_model(model_name: str = VERTEX_AI_SUMMARY_MODEL) -> GenerativeModel:
    """Get a Vertex AI generative model for summarization.

    Provider: Google Cloud Vertex AI (aiplatform.googleapis.com)
    Model: gemini-1.0-pro-002 (Google's production LLM)

    Available models:
        - gemini-1.0-pro-002: Text generation and summarization
        - gemini-1.5-pro-002: Enhanced multimodal model
        - text-bison: Legacy text model
    """
    return GenerativeModel(model_name)


def summarize_transcript_chunk(
    transcript: str,
    project_id: Optional[str] = None,
    model_name: str = VERTEX_AI_SUMMARY_MODEL,
    max_output_tokens: int = 256,
) -> str:
    """Summarize a meeting transcript chunk using Google Cloud Vertex AI.

    Provider: Google Cloud Vertex AI (aiplatform.googleapis.com)
    Model: gemini-1.0-pro-002

    Args:
        transcript: Meeting transcript text to summarize
        project_id: Google Cloud project ID
        model_name: Vertex AI model identifier
        max_output_tokens: Maximum tokens in summary output

    Returns:
        Summarized text string
    """
    initialize_vertex_ai(project_id=project_id)
    model = get_summary_model(model_name)

    prompt = f"""You are a meeting assistant. Summarize the following meeting transcript.
Focus on key decisions, action items, and important discussion points.
Keep the summary concise and structured.

Transcript:
{transcript}

Summary:"""

    response = model.generate_content(
        prompt,
        generation_config={
            "max_output_tokens": max_output_tokens,
            "temperature": 0.3,
        },
    )

    return response.text.strip() if response.text else ""


class MeetingSummarizer:
    """Incremental summarizer for live meeting transcripts.

    Provider: Google Cloud Vertex AI (aiplatform.googleapis.com)
    Model: gemini-1.0-pro-002
    """

    def __init__(
        self,
        project_id: Optional[str] = None,
        model_name: str = VERTEX_AI_SUMMARY_MODEL,
        chunk_size: int = 2000,
    ):
        self.project_id = project_id
        self.model_name = model_name
        self.chunk_size = chunk_size
        self._buffer = ""
        self._summaries: list[str] = []

    def add_transcript(self, transcript: str) -> Optional[str]:
        """Add transcript text and return a summary if buffer exceeds chunk size.

        Provider: Google Cloud Vertex AI (aiplatform.googleapis.com)
        Model: gemini-1.0-pro-002
        """
        self._buffer += " " + transcript if self._buffer else transcript

        if len(self._buffer) >= self.chunk_size:
            summary = summarize_transcript_chunk(
                self._buffer,
                project_id=self.project_id,
                model_name=self.model_name,
            )
            self._summaries.append(summary)
            self._buffer = ""
            return summary
        return None

    def finalize(self) -> Optional[str]:
        """Summarize any remaining buffered transcript.

        Provider: Google Cloud Vertex AI (aiplatform.googleapis.com)
        """
        if self._buffer.strip():
            summary = summarize_transcript_chunk(
                self._buffer,
                project_id=self.project_id,
                model_name=self.model_name,
            )
            self._summaries.append(summary)
            self._buffer = ""
            return summary
        return None

    @property
    def all_summaries(self) -> list[str]:
        """Return all generated summaries."""
        return list(self._summaries)

    @property
    def full_summary(self) -> str:
        """Return concatenated full summary."""
        return "\n\n".join(self._summaries)
