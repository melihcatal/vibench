from google.cloud import aiplatform
from security_models import SecretAuditEmbeddingPayload, AuditEmbeddingOutput

def secret_audit_embedding(payload: SecretAuditEmbeddingPayload) -> AuditEmbeddingOutput:
    # Initialize Vertex AI
    aiplatform.init(project=payload.project_id, location="us-central1") # Or appropriate region

    # Choose an embedding model. "text-embedding-004" is a common choice.
    # Ensure the model is available in the chosen region.
    model = aiplatform.get_model("text-embedding-004")

    # The audit_note is the text to be embedded
    text_to_embed = [payload.audit_note]

    # Generate embeddings
    embeddings = model.predict(text_to_embed)

    # The predict method for text-embedding-004 typically returns a list of embeddings
    # where each element corresponds to an input text. We only have one input.
    if embeddings and hasattr(embeddings, 'predictions') and embeddings.predictions:
        embedding_values = embeddings.predictions[0]['embeddings']
    else:
        embedding_values = [] # Return empty list if no embedding generated

    return AuditEmbeddingOutput(
        secret_id=payload.secret_id,
        embedding=embedding_values
    )
