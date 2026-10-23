import asyncio
import os
from typing import AsyncIterator, List

from google.cloud import aiplatform
from google.api_core.exceptions import GoogleAPIError

from speech_models import TranscriptResult, CaptionEmbeddingResult

PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT_ID", "your-gcp-project-id")
LOCATION = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")

EMBEDDING_MODEL_ID = "text-embedding-004"

async def embed_caption_chunks(
    caption_stream: AsyncIterator[TranscriptResult]
) -> AsyncIterator[CaptionEmbeddingResult]:
    if not PROJECT_ID or PROJECT_ID == "your-gcp-project-id":
        raise ValueError("GOOGLE_CLOUD_PROJECT_ID environment variable not set or is default. Please set it.")
    if not LOCATION or LOCATION == "us-central1":
        raise ValueError("GOOGLE_CLOUD_LOCATION environment variable not set or is default. Please set it.")

    aiplatform.init(project=PROJECT_ID, location=LOCATION)
    embedding_model = aiplatform.preview.language_models.TextEmbeddingModel.from_pretrained(EMBEDDING_MODEL_ID)

    async for transcript_result in caption_stream:
        if transcript_result.is_final and transcript_result.transcript.strip():
            try:
                embeddings_response = await embedding_model.get_embeddings_async([transcript_result.transcript])
                
                if embeddings_response and embeddings_response.embeddings:
                    embedding_values = embeddings_response.embeddings[0].values
                    yield CaptionEmbeddingResult(
                        text=transcript_result.transcript,
                        embedding=list(embedding_values)
                    )
            except GoogleAPIError as e:
                print(f"Vertex AI API error for embedding: {e}")
                continue
            except Exception as e:
                print(f"An unexpected error occurred during embedding: {e}")
                continue
