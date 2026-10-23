from openai import OpenAI
import os

def embed_audit_notes(audit_notes_text: str) -> list:
    """
    Embeds secret audit notes for semantic search using OpenAI Embeddings.
    Requires OPENAI_API_KEY environment variable.
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    client = OpenAI(api_key=api_key)
    embedding_model = "text-embedding-ada-002" # OpenAI's current recommended embedding model

    try:
        response = client.embeddings.create(input=[audit_notes_text], model=embedding_model)
        return response.data[0].embedding
    except Exception as e:
        print(f"Error generating OpenAI embedding: {e}")
        raise

if __name__ == '__main__':
    # Example usage (requires OPENAI_API_KEY environment variable)
    # os.environ['OPENAI_API_KEY'] = 'YOUR_OPENAI_API_KEY'
    sample_audit_note = "User 'john.doe' accessed production database secret for debugging purposes on 2023-10-26."
    try:
        embedding = embed_audit_notes(sample_audit_note)
        print(f"Embedding generated (first 5 values): {embedding[:5]}...")
        print(f"Embedding dimension: {len(embedding)}")
    except Exception:
        print("Failed to generate embedding.")
