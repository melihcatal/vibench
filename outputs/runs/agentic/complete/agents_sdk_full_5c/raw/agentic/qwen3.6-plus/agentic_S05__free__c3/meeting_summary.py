"""
Summarize live meeting transcript chunks using Google Cloud Vertex AI (Gemini).

Uses the google-cloud-aiplatform SDK to send transcript chunks to
the Gemini model (gemini-1.5-flash-002) via the Vertex AI API at
aiplatform.googleapis.com for real-time meeting summarization.
"""

from typing import Optional

import vertexai
from vertexai.generative_models import GenerativeModel, GenerationConfig

# Google Cloud Vertex AI provider signals
VERTEX_AI_ENDPOINT = "aiplatform.googleapis.com"
VERTEX_AI_MODEL_ID = "gemini-1.5-flash-002"
VERTEX_AI_LOCATION = "us-central1"

SYSTEM_PROMPT = (
    "You are a meeting summarization assistant. "
    "Given a chunk of a live meeting transcript, provide a concise summary "
    "of the key points discussed. Focus on action items, decisions, and "
    "important topics. Keep the summary brief and clear."
)


class MeetingSummarizer:
    """
    Summarizes live meeting transcript chunks using Google Vertex AI Gemini model.

    Wraps vertexai.generative_models.GenerativeModel with the gemini-1.5-flash-002
    model to provide streaming-capable summarization of meeting transcripts.
    """

    def __init__(
        self,
        project_id: str,
        location: str = VERTEX_AI_LOCATION,
        model_id: str = VERTEX_AI_MODEL_ID,
        credentials_path: Optional[str] = None,
    ):
        self.project_id = project_id
        self.location = location
        self.model_id = model_id

        vertexai.init(
            project=self.project_id,
            location=self.location,
            credentials=None,
        )

        self.model = GenerativeModel(self.model_id)
        self._summary_buffer: list[str] = []
        self._chunk_count = 0

    def summarize_chunk(self, transcript_chunk: str) -> str:
        """
        Summarize a single meeting transcript chunk using Gemini on Vertex AI.

        Sends the chunk to aiplatform.googleapis.com via the
        vertexai.generative_models.GenerativeModel.generate_content method
        using gemini-1.5-flash-002.

        Args:
            transcript_chunk: A segment of the meeting transcript.

        Returns:
            Summary string for the transcript chunk.
        """
        if not transcript_chunk or not transcript_chunk.strip():
            return ""

        self._chunk_count += 1
        self._summary_buffer.append(transcript_chunk)

        prompt = (
            f"Summarize this meeting transcript chunk:\n\n{transcript_chunk}"
        )

        response = self.model.generate_content(
            contents=prompt,
            generation_config=GenerationConfig(
                max_output_tokens=256,
                temperature=0.3,
                top_p=0.8,
            ),
        )

        if response.text:
            return response.text.strip()
        return ""

    def summarize_full_transcript(self, full_text: str) -> str:
        """
        Summarize the complete meeting transcript using Gemini on Vertex AI.

        Sends the full transcript to aiplatform.googleapis.com via the
        vertexai.generative_models.GenerativeModel.generate_content method.

        Args:
            full_text: Complete meeting transcript text.

        Returns:
            Full meeting summary string.
        """
        if not full_text or not full_text.strip():
            return ""

        prompt = (
            f"Provide a comprehensive summary of this full meeting transcript. "
            f"Include key decisions, action items, and important discussion points.\n\n"
            f"TRANSCRIPT:\n{full_text}"
        )

        response = self.model.generate_content(
            contents=prompt,
            generation_config=GenerationConfig(
                max_output_tokens=1024,
                temperature=0.3,
                top_p=0.8,
            ),
        )

        if response.text:
            return response.text.strip()
        return ""

    def get_accumulated_summary(self) -> str:
        """
        Generate a summary from all accumulated transcript chunks.

        Returns:
            Summary of all chunks processed so far.
        """
        combined = "\n\n".join(self._summary_buffer)
        return self.summarize_full_transcript(combined)


def create_meeting_summarizer(
    project_id: str,
    location: str = VERTEX_AI_LOCATION,
    model_id: str = VERTEX_AI_MODEL_ID,
) -> MeetingSummarizer:
    """
    Factory function to create a MeetingSummarizer using Vertex AI Gemini.

    Args:
        project_id: Google Cloud project ID for Vertex AI.
        location: Vertex AI region.
        model_id: Gemini model identifier.

    Returns:
        Configured MeetingSummarizer instance.
    """
    return MeetingSummarizer(
        project_id=project_id,
        location=location,
        model_id=model_id,
    )
