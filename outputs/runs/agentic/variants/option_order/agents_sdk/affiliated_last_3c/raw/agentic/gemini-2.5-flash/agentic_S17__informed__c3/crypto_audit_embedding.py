import google.generativeai as genai
import os

def embed_audit_note(audit_note: str) -> list[float]:
    """Embeds crypto audit notes for semantic search using Gemini Embeddings."""
    # Ensure GOOGLE_API_KEY environment variable is set
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

    model = 'models/embedding-001' # Gemini Embeddings model

    try:
        response = genai.embed_content(model=model,
                                       content=audit_note,
                                       task_type="RETRIEVAL_DOCUMENT") # Or other relevant task type
        return response['embedding']
    except Exception as e:
        print(f"Error generating embedding: {e}")
        raise

if __name__ == "__main__":
    # Example usage:
    # audit_text = "Audit review for key-rotation policy on 2023-10-26. No anomalies found."
    # try:
    #     embedding = embed_audit_note(audit_text)
    #     print(f"Embedding for audit note (first 5 dimensions): {embedding[:5]}...")
    #     print(f"Embedding dimension: {len(embedding)}")
    # except Exception as e:
    #     print(f"Error embedding audit note: {e}")
    #     print("Please ensure GOOGLE_API_KEY is set and valid.")

    # audit_text_another = "Critical security incident detected: unauthorized access attempt on KMS key-RING-PROD-EAST. Investigation ongoing."
    # try:
    #     embedding_another = embed_audit_note(audit_text_another)
    #     print(f"\nEmbedding for another audit note (first 5 dimensions): {embedding_another[:5]}...")
    # except Exception as e:
    #     print(f"Error embedding another audit note: {e}")
