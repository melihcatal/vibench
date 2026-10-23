import os
from google.cloud import aiplatform

def embed_for_search(query: str, documents: list[str]) -> dict:
    project_id = os.getenv("GCP_PROJECT_ID")
    location = os.getenv("GCP_LOCATION", "us-central1")

    if not project_id:
        raise ValueError("GCP_PROJECT_ID environment variable not set.")

    aiplatform.init(project=project_id, location=location)

    # Using text-embedding-004, a Google Cloud Vertex AI model
    model = aiplatform.get_model("text-embedding-004")

    query_embedding_response = model.predict(instances=[{"content": query}])
    query_embedding = query_embedding_response.predictions[0]["embeddings"]["values"]

    document_embeddings = []
    if documents:
        document_instances = [{"content": doc} for doc in documents]
        document_batch_embedding_response = model.predict(instances=document_instances)
        for prediction in document_batch_embedding_response.predictions:
            document_embeddings.append(prediction["embeddings"]["values"])

    return {
        "query_embedding": query_embedding,
        "document_embeddings": document_embeddings,
    }
