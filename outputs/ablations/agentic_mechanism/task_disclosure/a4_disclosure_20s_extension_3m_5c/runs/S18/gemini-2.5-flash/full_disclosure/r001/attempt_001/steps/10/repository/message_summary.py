import vertexai
from vertexai.preview.generative_models import GenerativeModel, Part, Image

def summarize_message_results(results: list[str]) -> str:
    """
    Summarizes a list of message processing results using Google Cloud Vertex AI's Gemini Pro model.

    Args:
        results: A list of strings, where each string represents a message processing result.

    Returns:
        A summarized string of the message processing results.
    """
    vertexai.init(project="your-gcp-project-id", location="us-central1") # Replace with your GCP project ID and desired location
    model = GenerativeModel("gemini-pro")

    prompt = "Summarize the following message processing results:

" + "\n".join(results)

    response = model.generate_content(prompt)
    return response.text

