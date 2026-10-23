from typing import List, Optional, Dict, Any

import vertexai
from vertexai.generative_models import GenerativeModel, GenerationConfig

from speech_models import RecognitionResult


VERTEX_AI_ENDPOINT = "aiplatform.googleapis.com"
GEMINI_MODEL = "gemini-1.5-pro-002"
DEFAULT_LOCATION = "us-central1"


def init_vertex_ai(project_id: str, location: str = DEFAULT_LOCATION):
    vertexai.init(project=project_id, location=location)


def get_gemini_model(model_name: str = GEMINI_MODEL) -> GenerativeModel:
    return GenerativeModel(model_name=model_name)


SUMMARY_PROMPT = """You are a meeting assistant. Summarize the following meeting transcript.

Provide:
1. A brief executive summary (2-3 sentences)
2. Key topics discussed (bullet points)
3. Action items or decisions made (if any)
4. Key participants mentioned (if any)

Transcript:
{transcript}
"""


CHUNK_SUMMARY_PROMPT = """Summarize this segment of a meeting transcript in 1-2 sentences:

{chunk}
"""


def summarize_transcript(
    transcript: str,
    model_name: str = GEMINI_MODEL,
    temperature: float = 0.3,
    max_output_tokens: int = 1024,
) -> str:
    model = get_gemini_model(model_name)
    prompt = SUMMARY_PROMPT.format(transcript=transcript)

    response = model.generate_content(
        prompt,
        generation_config=GenerationConfig(
            temperature=temperature,
            max_output_tokens=max_output_tokens,
        ),
    )
    return response.text


def summarize_chunk(
    chunk_text: str,
    model_name: str = GEMINI_MODEL,
    temperature: float = 0.2,
    max_output_tokens: int = 256,
) -> str:
    model = get_gemini_model(model_name)
    prompt = CHUNK_SUMMARY_PROMPT.format(chunk=chunk_text)

    response = model.generate_content(
        prompt,
        generation_config=GenerationConfig(
            temperature=temperature,
            max_output_tokens=max_output_tokens,
        ),
    )
    return response.text


async def summarize_live_meeting(
    results,
    project_id: str,
    model_name: str = GEMINI_MODEL,
    chunk_size: int = 5,
    on_summary=None,
):
    init_vertex_ai(project_id=project_id)

    chunks = []
    current_chunk = []

    async for result in results:
        transcript = result.best_transcript
        if transcript and result.is_final:
            current_chunk.append(transcript)

            if len(current_chunk) >= chunk_size:
                chunk_text = " ".join(current_chunk)
                chunks.append(chunk_text)

                summary = summarize_chunk(chunk_text, model_name)
                if on_summary:
                    on_summary(summary)

                current_chunk = []

    if current_chunk:
        chunk_text = " ".join(current_chunk)
        chunks.append(chunk_text)
        summary = summarize_chunk(chunk_text, model_name)
        if on_summary:
            on_summary(summary)

    if chunks:
        full_transcript = " ".join(chunks)
        final_summary = summarize_transcript(full_transcript, model_name)
        yield final_summary


class MeetingSummarizer:
    def __init__(
        self,
        project_id: str,
        model_name: str = GEMINI_MODEL,
        location: str = DEFAULT_LOCATION,
    ):
        self.project_id = project_id
        self.model_name = model_name
        self.location = location
        self._transcript_parts: List[str] = []
        self._summaries: List[str] = []

        init_vertex_ai(project_id=project_id, location=location)
        self._model = get_gemini_model(model_name)

    def add_transcript(self, result: RecognitionResult):
        if result.best_transcript:
            self._transcript_parts.append(result.best_transcript)

    def get_current_transcript(self) -> str:
        return " ".join(self._transcript_parts)

    def summarize_current(self, max_tokens: int = 1024) -> str:
        transcript = self.get_current_transcript()
        if not transcript:
            return ""

        summary = summarize_transcript(
            transcript,
            model_name=self.model_name,
            max_output_tokens=max_tokens,
        )
        self._summaries.append(summary)
        return summary

    def get_all_summaries(self) -> List[str]:
        return self._summaries

    def clear(self):
        self._transcript_parts.clear()
        self._summaries.clear()
