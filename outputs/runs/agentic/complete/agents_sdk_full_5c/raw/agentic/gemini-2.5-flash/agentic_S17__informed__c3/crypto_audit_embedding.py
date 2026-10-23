import os
import google.generativeai as genai
from typing import List
from security_client import configure_gemini_api
from security_models import EmbeddingRequest, EmbeddingResponse

def embed_audit_note(request: EmbeddingRequest) -> EmbeddingResponse:
    """Generates embeddings for a crypto audit note using Google Gemini Embeddings."""
    configure_gemini_api()
    
    # The embedding model to use. For text embeddings, 'models/embedding-001' is common.
    embedding_model = 'models/embedding-001'

    result = genai.embed_content(
        model=embedding_model,
        content=request.text_content,
        task_type="RETRIEVAL_DOCUMENT" # or other task types like RETRIEVAL_QUERY, SEMANTIC_SIMILARITY, etc.
    )

    # The result contains a list of floats as the embedding vector
    embedding_vector: List[float] = result['embedding']
    
    return EmbeddingResponse(embedding=embedding_vector)

if __name__ == '__main__':
    # Example Usage
    # Ensure GOOGLE_API_KEY environment variable is set.

    sample_audit_note_1 = "Audit log: Key 'app-enc-key' used for 120 encryptions and 115 decryptions today. All successful."
    sample_audit_note_2 = "Audit log: Anomalous activity detected on 'auth-sign-key'. Multiple failed sign attempts from unknown IP."
    sample_audit_note_3 = "System health check passed. All encryption services operational."

    try:
        print("Generating embedding for audit note 1 with Gemini Embeddings...")
        request_1 = EmbeddingRequest(text_content=sample_audit_note_1)
        embedding_response_1 = embed_audit_note(request_1)
        print(f"Embedding for Note 1 (first 5 values): {embedding_response_1.embedding[:5]}...")
        print(f"Embedding length: {len(embedding_response_1.embedding)}")

        print("\nGenerating embedding for audit note 2 with Gemini Embeddings...")
        request_2 = EmbeddingRequest(text_content=sample_audit_note_2)
        embedding_response_2 = embed_audit_note(request_2)
        print(f"Embedding for Note 2 (first 5 values): {embedding_response_2.embedding[:5]}...")

        print("\nGenerating embedding for audit note 3 with Gemini Embeddings...")
        request_3 = EmbeddingRequest(text_content=sample_audit_note_3)
        embedding_response_3 = embed_audit_note(request_3)
        print(f"Embedding for Note 3 (first 5 values): {embedding_response_3.embedding[:5]}...")

    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
