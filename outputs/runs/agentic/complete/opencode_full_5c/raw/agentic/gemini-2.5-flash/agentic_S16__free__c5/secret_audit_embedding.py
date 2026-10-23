import os
import google.generativeai as genai
from typing import List

# Ensure you have your Google API key set as an environment variable (e.g., GOOGLE_API_KEY)
API_KEY = os.environ.get("GOOGLE_API_KEY")


def embed_audit_notes(audit_notes: List[str]) -> List[List[float]]:
    if not API_KEY:
        raise ValueError(
            "GOOGLE_API_KEY environment variable not set for Generative AI."
        )

    genai.configure(api_key=API_KEY)

    # Use the text-embedding-004 model for embeddings
    model = "models/text-embedding-004"

    # The embedding model expects a list of strings
    response = genai.embed_content(
        model=model, content=audit_notes, task_type="RETRIEVAL_DOCUMENT"
    )
    return response["embedding"]


# Example Usage
if __name__ == "main":
    try:
        notes_to_embed = [
            "Secret rotation performed by security team on 2023-10-26 due to compliance.",
            "Automated rotation failed on 2023-10-25, manual intervention required.",
            "New secret version added for database connection string.",
        ]
        embeddings = embed_audit_notes(notes_to_embed)
        print(
            f"Generated {len(embeddings)} embeddings. First embedding snippet: {embeddings[0][:5]}..."
        )
    except Exception as e:
        print(f"Error generating embeddings: {e}")
