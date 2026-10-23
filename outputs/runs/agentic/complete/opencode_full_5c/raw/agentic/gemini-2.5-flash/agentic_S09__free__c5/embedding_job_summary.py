import os
from typing import List, Dict, Any
from google.cloud import aiplatform

from embeddings_client import get_vertex_ai_publisher_client


def summarize_embedding_job_results(results: List[Dict[str, Any]]) -> str:
    """Summarizes embedding job results using Vertex AI Generative AI (Gemini Pro).

    Args:
        results: A list of dictionaries, where each dictionary represents an embedding result,
                 e.g., {'text': '...', 'embedding': [...]}.

    Returns:
        A string summarizing the embedding job results.
    """
    client = get_vertex_ai_publisher_client()
    project_id = os.environ.get("GCP_PROJECT_ID")
    model_id = "gemini-pro"

    prompt_text = """
    Summarize the following embedding job results. Highlight any interesting patterns or anomalies.

    Embedding Job Results:
    """

    for i, result in enumerate(results):
        prompt_text += f"\nItem {i + 1}: Text: '{result['text']}', Embedding (first 5 values): {result['embedding'][:5]}..."

    # The actual endpoint resource name for generative models is typically:
    # projects/<project_id>/locations/<location>/publishers/google/models/<model_id>
    model_endpoint = f"projects/{project_id}/locations/us-central1/publishers/google/models/{model_id}"

    # The instances for generative models are typically a list of dicts with 'prompt' key
    instances = [{"prompt": prompt_text}]

    response = client.predict(endpoint=model_endpoint, instances=instances)
    summary = response.predictions[0]["candidates"][0]["content"].strip()

    return summary
