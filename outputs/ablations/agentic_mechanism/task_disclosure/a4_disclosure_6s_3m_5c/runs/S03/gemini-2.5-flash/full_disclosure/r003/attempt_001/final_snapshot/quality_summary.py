import os
from google.cloud import aiplatform
from vertexai.preview.generative_models import GenerativeModel, Part, Image

def summarize_quality_issues(issues: list[str]) -> str:
    """
    Summarizes translation quality issues using Google Cloud Vertex AI.

    Args:
        issues: A list of strings, each describing a translation quality issue.

    Returns:
        A summarized string of the translation quality issues.
    """
    # Initialize Vertex AI
    aiplatform.init(project=os.environ.get("GOOGLE_CLOUD_PROJECT"), location=os.environ.get("GOOGLE_CLOUD_REGION"))

    # Load the generative model
    model = GenerativeModel("gemini-pro")

    # Construct the prompt
    prompt = "Summarize the following translation quality issues:
" + "\n".join(issues)

    # Generate content
    response = model.generate_content(prompt)

    return response.text
