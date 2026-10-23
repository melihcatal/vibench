import json
from ibm_watsonx_ai import WMLClient
from observability_client import get_watsonx_embedding_config


def embed_log_messages(log_events):
    """
    Embed selected log messages using watsonx.ai text embeddings for semantic retrieval.

    Parameters
    ----------
    log_events: list[dict]
        Log entries that contain a 'message' field to embed.

    Returns
    -------
    list[float]
        List of embedding vectors (as lists of floats) corresponding to each log event.
    """
    config = get_watsonx_embedding_config()
    service_url = config["endpoint"]
    api_key = config["api_key"]
    project_id = config["project_id"]
    client = WMLClient(service_url, api_key, project_id)
    embeddings = []
    for ev in log_events:
        msg = ev.get("message", "")
        # Call watsonx embeddings endpoint via SDK
        response = client.get_text_embedding(text=msg)
        vectors = response["embeddings"][0]["vector"]  # list of floats
        embeddings.append(vectors)
    return embeddings
