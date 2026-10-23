import asyncio
import os
from typing import AsyncIterator, List

from google.cloud import aiplatform
from google.api_core.exceptions import GoogleAPIError

from speech_models import TranscriptResult, MeetingSummaryResult

PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT_ID", "your-gcp-project-id")
LOCATION = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")

MODEL_NAME = "gemini-pro"

async def summarize_meeting_chunks(
    caption_stream: AsyncIterator[TranscriptResult],
    min_chunk_size: int = 500
) -> AsyncIterator[MeetingSummaryResult]:
    if not PROJECT_ID or PROJECT_ID == "your-gcp-project-id":
        raise ValueError("GOOGLE_CLOUD_PROJECT_ID environment variable not set or is default. Please set it.")
    if not LOCATION or LOCATION == "us-central1":
        raise ValueError("GOOGLE_CLOUD_LOCATION environment variable not set or is default. Please set it.")

    aiplatform.init(project=PROJECT_ID, location=LOCATION)
    model = aiplatform.preview.generative_models.GenerativeModel(MODEL_NAME)

    accumulated_transcript: List[str] = []
    current_text_length = 0

    async for transcript_result in caption_stream:
        if transcript_result.is_final and transcript_result.transcript.strip():
            accumulated_transcript.append(transcript_result.transcript)
            current_text_length += len(transcript_result.transcript)

            if current_text_length >= min_chunk_size:
                text_to_summarize = " ".join(accumulated_transcript)
                prompt = f"Summarize the following meeting transcript:\n\n{text_to_summarize}\n\nSummary:"
                
                try:
                    response = model.generate_content([prompt])
                    summary = response.text
                    if summary:
                        yield MeetingSummaryResult(
                            summary_text=summary.strip(),
                            source_text=text_to_summarize
                        )

                    accumulated_transcript = []
                    current_text_length = 0

                except GoogleAPIError as e:
                    print(f"Vertex AI API error for summarization: {e}")
                    continue
                except Exception as e:
                    print(f"An unexpected error occurred during summarization: {e}")
                    continue

    if accumulated_transcript and current_text_length > 0:
        text_to_summarize = " ".join(accumulated_transcript)
        prompt = f"Summarize the following meeting transcript:\n\n{text_to_summarize}\n\nSummary:"
        try:
            response = model.generate_content([prompt])
            summary = response.text
            if summary:
                yield MeetingSummaryResult(
                    summary_text=summary.strip(),
                    source_text=text_to_summarize
                )
        except GoogleAPIError as e:
            print(f"Vertex AI API error for final summarization: {e}")
        except Exception as e:
            print(f"An unexpected error occurred during final summarization: {e}")
