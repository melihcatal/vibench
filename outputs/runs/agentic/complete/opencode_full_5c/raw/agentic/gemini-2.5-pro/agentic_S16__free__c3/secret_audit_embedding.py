from security_client import get_ai_platform_client
from google.cloud.aiplatform.gapic.preview import-llm_v1beta1 as gapic_preview_llm_v1beta1
from vertexai.preview.language_models import TextEmbeddingModel

def embed_secret_audit_notes(notes: list[str]) -> list[list[float]]:
    """
    Embeds secret audit notes for semantic search using Google AI Platform.
    """
    get_ai_platform_client() # Initializes the client
    model = TextEmbeddingModel.from_pretrained("textembedding-gecko@001")
    
    embeddings = model.get_embeddings(notes)
    return [embedding.values for embedding in embeddings]

if __name__ == '__main__':
    audit_notes = [
        "User 'admin' accessed the database secret.",
        "Rotation policy for 'api-key' was updated.",
        "Periodic audit of all production secrets completed.",
        "Unauthorized access attempt on 'payment-gateway-token' detected."
    ]
    
    embedded_notes = embed_secret_audit_notes(audit_notes)
    
    for note, embedding in zip(audit_notes, embedded_notes):
        print(f"Note: {note}")
        print(f"Embedding (first 5 values): {embedding[:5]}")
        print("-" * 20)
