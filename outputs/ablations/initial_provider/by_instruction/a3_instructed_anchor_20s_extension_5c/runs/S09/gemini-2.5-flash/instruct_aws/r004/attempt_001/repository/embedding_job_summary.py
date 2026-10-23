import json
from typing import Any
from google.cloud import aiplatform

# Initialize Vertex AI
aiplatform.init(project="your-gcp-project-id", location="us-central1")

def summarize_embedding_job_results(job_results: list[dict[str, Any]]) -> str:
    """
    Summarizes embedding job results using Google Cloud's Generative AI.
    
    Args:
        job_results: A list of dictionaries, where each dictionary represents
                     a job result. It should contain at least 'text' and 'embedding' keys.

    Returns:
        A string summarizing the embedding job results.
    """
    model = aiplatform.preview.generative_models.GenerativeModel("gemini-pro")

    # Prepare the prompt for summarization
    # For simplicity, we'll just take a few text samples to summarize their embedding process
    texts_to_summarize = [result.get("text", "") for result in job_results[:5]] # Take up to 5 texts
    if not texts_to_summarize:
        return "No embedding job results to summarize."
    
    input_text = "Please summarize the following texts, which were recently processed for generating vector embeddings: " \
                 + "; ".join(texts_to_summarize)

    response = model.generate_content([input_text])
    return response.text
