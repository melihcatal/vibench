import asyncio
import os
from typing import AsyncIterator, List

from google.cloud import aiplatform
from google.api_core.exceptions import GoogleAPIError

from speech_models import TranscriptResult, SafetyDetectionResult

PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT_ID", "your-gcp-project-id")
LOCATION = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")

MODEL_NAME = "gemini-pro"

async def check_live_caption_safety(
    caption_stream: AsyncIterator[TranscriptResult]
) -> AsyncIterator[SafetyDetectionResult]:
    if not PROJECT_ID or PROJECT_ID == "your-gcp-project-id":
        raise ValueError("GOOGLE_CLOUD_PROJECT_ID environment variable not set or is default. Please set it.")
    if not LOCATION or LOCATION == "us-central1":
        raise ValueError("GOOGLE_CLOUD_LOCATION environment variable not set or is default. Please set it.")

    aiplatform.init(project=PROJECT_ID, location=LOCATION)
    model = aiplatform.preview.generative_models.GenerativeModel(MODEL_NAME)

    async for transcript_result in caption_stream:
        if transcript_result.is_final and transcript_result.transcript.strip():
            try:
                response = model.generate_content([transcript_result.transcript])

                is_safe = True
                categories: List[str] = []
                scores: List[float] = []

                if response.prompt_feedback and response.prompt_feedback.safety_ratings:
                    for rating in response.prompt_feedback.safety_ratings:
                        if rating.probability >= aiplatform.genai.preview.generative_models.HarmProbability.MEDIUM:
                            is_safe = False
                            categories.append(rating.category.name.lower().replace("_", " ").replace("harm category ", ""))
                            scores.append(rating.probability.value)

                yield SafetyDetectionResult(
                    text=transcript_result.transcript,
                    categories=categories,
                    scores=scores,
                    is_safe=is_safe
                )
            except GoogleAPIError as e:
                print(f"Vertex AI API error for safety check: {e}")
                yield SafetyDetectionResult(
                    text=transcript_result.transcript,
                    categories=["error"],
                    scores=[1.0],
                    is_safe=False
                )
            except Exception as e:
                print(f"An unexpected error occurred during safety check: {e}")
                yield SafetyDetectionResult(
                    text=transcript_result.transcript,
                    categories=["unknown_error"],
                    scores=[1.0],
                    is_safe=False
                )
