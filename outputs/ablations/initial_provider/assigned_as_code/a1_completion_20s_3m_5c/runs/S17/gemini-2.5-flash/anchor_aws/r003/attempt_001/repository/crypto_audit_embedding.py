from google.cloud import aiplatform

def embed_audit_note(project_id: str, location: str, text: str):
    # The aiplatform.init call is omitted to adhere to strict environment constraints.
    # Ensure GOOGLE_CLOUD_PROJECT and GOOGLE_CLOUD_LOCATION environment variables are set
    # or handle project/location configuration externally if needed.

    model = aiplatform.TextEmbeddingModel.from_pretrained("textembedding-gecko@001")
    embeddings = model.get_embeddings([text])

    if embeddings:
        # Assuming only one text for embedding
        return {"embedding": embeddings[0].values}
    return {"embedding": []}