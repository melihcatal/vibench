import os
from google.cloud import aiplatform


def summarize_meeting_chunk(
    text_chunk: str, project_id: str = None, location: str = "us-central1"
) -> str:
    """Summarizes a chunk of live meeting transcript using Google Cloud Generative AI (Gemini Pro).

    Args:
        text_chunk: A segment of the meeting transcript to summarize.
        project_id: Your Google Cloud project ID. If None, it will be inferred from the environment.
        location: The Google Cloud region where the Vertex AI model is deployed.

    Returns:
        A concise summary of the text chunk.
    """
    if project_id is None:
        project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
        if not project_id:
            raise ValueError(
                "Google Cloud project ID must be provided or set in GOOGLE_CLOUD_PROJECT environment variable."
            )

    aiplatform.init(project=project_id, location=location)

    from vertexai.preview.generative_models import GenerativeModel, Part

    model = GenerativeModel("gemini-pro")

    response = model.generate_content(
        [
            Part.from_text(
                f"Summarize the following meeting transcript chunk in one concise sentence: {text_chunk}"
            )
        ],
        generation_config={
            "temperature": 0.2,
            "max_output_tokens": 100,
        },
    )

    return response.text.strip()
