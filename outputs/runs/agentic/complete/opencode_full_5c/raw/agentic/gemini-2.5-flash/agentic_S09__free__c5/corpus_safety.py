import os
from typing import List, Dict, Any
from google.cloud.aiplatform_v1.types import PredictRequest

from embeddings_client import get_vertex_ai_publisher_client

SAFETY_MODEL_ID = "gemini-pro"


def check_corpus_safety(texts: List[str]) -> List[Dict[str, Any]]:
    """Checks corpus text for safety attributes before embedding using Vertex AI.

    Args:
        texts: A list of text strings from the corpus.

    Returns:
        A list of dictionaries, each containing safety attributes for the corresponding text.
    """
    client = get_vertex_ai_publisher_client()
    project_id = os.environ.get("GCP_PROJECT_ID")

    # For safety attributes, we can leverage the same model used for summarization (gemini-pro)
    # and craft a prompt to request safety analysis, or use a specific safety model if available.
    # For this exercise, we'll use gemini-pro and prompt for safety attributes.
    model_endpoint = f"projects/{project_id}/locations/us-central1/publishers/google/models/{SAFETY_MODEL_ID}"

    safety_results = []
    for text in texts:
        prompt_text = f"Analyze the safety attributes of the following text: '{text}'. Provide a brief assessment of categories like toxicity, hate speech, sexual content, dangerous content, and any other relevant safety scores. Format as JSON."
        instances = [{"prompt": prompt_text}]
        response = client.predict(endpoint=model_endpoint, instances=instances)
        # Assuming the response for safety is within the 'content' of the first candidate
        # and needs to be parsed as JSON if the model is prompted to produce JSON.
        # In a real scenario, a dedicated safety API would return structured data.
        try:
            # This is a simplification; a real safety API would return structured safety scores.
            # We are asking Gemini to describe safety attributes as text.
            safety_assessment = response.predictions[0]["candidates"][0][
                "content"
            ].strip()
            safety_results.append(
                {"text": text, "safety_assessment": safety_assessment}
            )
        except (KeyError, IndexError):
            safety_results.append(
                {
                    "text": text,
                    "safety_assessment": "Could not retrieve safety assessment.",
                }
            )

    return safety_results
