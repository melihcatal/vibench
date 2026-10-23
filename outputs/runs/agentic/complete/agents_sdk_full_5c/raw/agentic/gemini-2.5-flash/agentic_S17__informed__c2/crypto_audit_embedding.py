import os
import google.generativeai as genai

from security_models import EmbeddingRequest, EmbeddingResult

def embed_crypto_audit_note(request: EmbeddingRequest) -> EmbeddingResult:
    """Embeds crypto audit notes for semantic search using Google Gemini Embeddings."""
    genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

    # Using a specific embedding model from the Gemini family
    # The model name should be concrete and identifiable
    embedding_model = "models/embedding-001"

    response = genai.embed_content(
        model=embedding_model,
        content=request.text,
        task_type="RETRIEVAL_DOCUMENT" # or other suitable task_type
    )

    # The embedding is usually a list of floats
    embedding = response["embedding"]
    return EmbeddingResult(embedding=embedding)

if __name__ == "__main__":
    # Example usage (requires GOOGLE_API_KEY env var)
    # from dotenv import load_dotenv
    # load_dotenv()
    # 
    # audit_note_req = EmbeddingRequest(text="Key rotation successful for KMS key ring 'production-keys'.")
    # embedding_result = embed_crypto_audit_note(audit_note_req)
    # print(f"Embedding (first 5 dims): {embedding_result.embedding[:5]}...")
    # print(f"Embedding dimension: {len(embedding_result.embedding)}")
    pass
