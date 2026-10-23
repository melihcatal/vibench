from google.cloud import aiplatform

def transcript_embedding(text, project_id, location="us-central1"):
    aiplatform.init(project=project_id, location=location)

    # Using a text-embedding-gecko model for embeddings
    # Model ID: "text-embedding-gecko@001" or similar
    # Note: Specific model versions might change, this is an example.
    model = aiplatform.TextEmbeddingModel.from_pretrained("text-embedding-gecko")
    embeddings = model.get_embeddings([text])

    return {"embedding": embeddings[0].values}
