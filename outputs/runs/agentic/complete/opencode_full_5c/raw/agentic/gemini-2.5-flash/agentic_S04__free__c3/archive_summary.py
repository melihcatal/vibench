import vertexai
from vertexai.preview.generative_models import GenerativeModel, Part, Image
from speech_models import SummarizationRequest


def summarize_transcript_results(request: SummarizationRequest) -> str:
    """Summarizes transcription results using a Google Cloud Generative AI model (Gemini)."""
    # TODO: Replace with your Google Cloud Project ID and region
    vertexai.init(project="your-google-cloud-project-id", location="us-central1")

    model = GenerativeModel("gemini-pro")  # Or "gemini-1.0-pro"

    prompt = f"Please summarize the following transcript: {request.text_content}"

    response = model.generate_content(prompt)

    return response.text
