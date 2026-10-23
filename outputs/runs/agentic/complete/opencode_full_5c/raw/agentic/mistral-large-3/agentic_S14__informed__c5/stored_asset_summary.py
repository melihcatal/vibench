from google.cloud import aiplatform
from dataclasses import dataclass
from typing import Optional


@dataclass
class SummaryResponse:
    summary: str
    model: str
    token_count: int


def stored_asset_summary(
    text: str,
    project_id: str,
    location: str = "us-central1",
    model_id: str = "google/flan-t5-xl",
) -> SummaryResponse:
    """
    Summarizes content extracted from a stored asset using Google Vertex AI.

    Args:
        text: Text to summarize.
        project_id: Google Cloud project ID.
        location: Vertex AI location (e.g., "us-central1").
        model_id: Vertex AI model ID (e.g., "google/flan-t5-xl").

    Returns:
        SummaryResponse containing the summary, model used, and token count.
    """
    aiplatform.init(project=project_id, location=location)
    model = aiplatform.TextGenerationModel.from_pretrained(model_id)

    response = model.predict(
        instances=[{"content": text}],
        parameters={
            "temperature": 0.2,
            "max_output_tokens": 256,
            "top_p": 0.8,
            "top_k": 40,
        },
    )

    return SummaryResponse(
        summary=response.predictions[0]["content"],
        model=model_id,
        token_count=response.predictions[0]["token_count"],
    )
