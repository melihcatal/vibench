import os
from observability_models import LogEvent
from google.cloud import aiplatform


def embed_log_messages(
    messages: list[str], model_id: str = "textembedding-gecko"
) -> list[list[float]]:
    """Embed selected log messages using Google Gemini Embeddings via Vertex AI.
    Returns a list of embedding vectors (list of floats).
    """
    aiplatform.init(project=os.getenv("WATSONX_PROJECT_ID"), location="us-central1")
    embeddings = aiplatform.Embeddings(model=model_id)
    response = embeddings.embed_content(messages)
    return [vec.embedding for vec in response]


# Example usage within a log processing function
# logs = [LogEvent(...), ...]
# vectors = embed_log_messages([log['message'] for log in logs])
