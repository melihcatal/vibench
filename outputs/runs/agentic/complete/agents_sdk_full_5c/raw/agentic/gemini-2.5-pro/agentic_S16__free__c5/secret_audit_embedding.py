
import os
from openai import OpenAI

def get_embedding_for_text(text: str, model: str = "text-embedding-3-small") -> list[float] | None:
    """
    Generates a vector embedding for a given text using OpenAI's API.

    Args:
        text: The input text to embed.
        model: The model to use for the embedding.

    Returns:
        A list of floats representing the embedding, or None on failure.
    """
    try:
        # The client uses the OPENAI_API_KEY environment variable by default.
        client = OpenAI()
        
        response = client.embeddings.create(
            input=text,
            model=model
        )
        
        return response.data[0].embedding
    except Exception as e:
        print(f"Error creating embedding with OpenAI: {e}")
        return None


if __name__ == '__main__':
    # Example usage:
    # Ensure the OPENAI_API_KEY environment variable is set.
    
    audit_note = (
        "User 'admin' rotated the 'prod/db/credentials' secret at 2023-10-27 10:00:00 UTC. "
        "Rotation was successful. The new version is 5. "
        "Reason: Scheduled quarterly rotation."
    )

    embedding = get_embedding_for_text(audit_note)

    if embedding:
        print(f"Successfully generated embedding for the audit note.")
        print(f"Embedding vector dimension: {len(embedding)}")
        # print("First 5 dimensions:", embedding[:5])
    else:
        print("Failed to generate embedding.")

