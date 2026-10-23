import os
import google.generativeai as genai
from typing import List

# Configure the Gemini API client
genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

def embed_audit_notes(notes: List[str]) -> List[List[float]]:
    """Embeds a list of secret audit notes using Google Gemini Embeddings.
    Returns a list of embedding vectors.
    """
    if not genai.get_default_api_key():
        raise ValueError("GOOGLE_API_KEY environment variable not set or configured.")

    # Use the 'embedding-001' model for embeddings
    # https://ai.google.dev/models/gemini#text-embedding
    response = genai.embed_content(
        model="models/embedding-001",
        content=notes,
        task_type="RETRIEVAL_DOCUMENT"
    )
    return [embedding.to_list() for embedding in response['embedding']]

if __name__ == "__main__":
    # Example usage
    audit_notes_to_embed = [
        "Access to production database secret was granted to a new SRE team member. Reviewed by Lead Engineer on 2023-11-15.",
        "Automated rotation of API key for Payment Gateway successful. Old version retired. No issues detected in monitoring logs.",
        "Attempted unauthorized access to analytics dashboard secret detected from an external IP. Alert triggered and blocked. Investigation ongoing.",
        "Secret for internal microservice authentication updated due to compliance requirement. All dependent services reconfigured."
    ]

    try:
        embeddings = embed_audit_notes(audit_notes_to_embed)
        print(f"Successfully generated {len(embeddings)} embeddings.")
        print(f"First embedding (truncated): {embeddings[0][:5]}...")

        # You can then store these embeddings in a vector database for semantic search
    except ValueError as e:
        print(f"Configuration Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
