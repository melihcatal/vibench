import os

from google.cloud import aiplatform
from vertexai.preview.language_models import TextGenerationModel


def summarize_meeting_chunks(transcript_chunks: list[str]) -> str:
    """Summarizes live meeting transcript chunks using Google Cloud Vertex AI Text Generation."""
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    if "GOOGLE_APPLICATION_CREDENTIALS" not in os.environ:
        print(
            "Warning: GOOGLE_APPLICATION_CREDENTIALS environment variable not set for Vertex AI."
        )

    # Initialize Vertex AI
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT", "your-project-id")
    location = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
    aiplatform.init(project=project_id, location=location)

    model = TextGenerationModel.from_pretrained(
        "text-bison@002"
    )  # Using text-bison for summarization

    full_transcript = " ".join(transcript_chunks)

    prompt = (
        f"Summarize the following meeting transcript:\n\n{full_transcript}\n\nSummary:"
    )

    try:
        response = model.predict(
            prompt,
            max_output_tokens=256,  # Adjust as needed for summary length
            temperature=0.2,  # Lower temperature for more factual summaries
        )
        return response.text
    except Exception as e:
        return f"Error during summarization: {str(e)}"
