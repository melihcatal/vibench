import os
from google.cloud import aiplatform

def embed_text_with_vertex_ai(texts: list[str], project_id: str, location: str, model_name: str = "text-embedding-004") -> list[list[float]]:
    """Generates embedding vectors for a list of text strings using Vertex AI.

    Args:
        texts: A list of text strings to embed.
        project_id: The Google Cloud project ID.
        location: The Google Cloud region (e.g., "us-central1").
        model_name: The name of the embedding model to use.

    Returns:
        A list of embedding vectors, where each vector is a list of floats.
    """
    aiplatform.init(project=project_id, location=location)
    model = aiplatform.gapic.PredictionServiceClient(client_options={"api_endpoint": f"{location}-aiplatform.googleapis.com"})
    endpoint = f"projects/{project_id}/locations/{location}/publishers/google/models/{model_name}"

    instances = [{"content": text} for text in texts]
    parameters = {"auto_truncate": True, "output_dimensionality": 768} # Example parameters, adjust as needed

    response = model.predict(endpoint=endpoint, instances=instances, parameters=parameters)

    embeddings = []
    for prediction in response.predictions:
        embeddings.append(prediction["embeddings"]["values"])
    return embeddings

def embed_for_search(query: str, documents: list[str], project_id: str, location: str, model_name: str = "text-embedding-004") -> tuple[list[float], list[list[float]]]:
    """Embeds a query and a list of documents for semantic search using Vertex AI.

    Args:
        query: The query string to embed.
        documents: A list of document strings to embed.
        project_id: The Google Cloud project ID.
        location: The Google Cloud region (e.g., "us-central1").
        model_name: The name of the embedding model to use.

    Returns:
        A tuple containing:
        - The embedding vector for the query (list of floats).
        - A list of embedding vectors for the documents (list of lists of floats).
    """
    all_texts = [query] + documents
    all_embeddings = embed_text_with_vertex_ai(all_texts, project_id, location, model_name)

    query_embedding = all_embeddings[0]
    document_embeddings = all_embeddings[1:]

    return query_embedding, document_embeddings

