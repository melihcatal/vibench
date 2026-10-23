import os
from openai import OpenAI

def get_embedding(text: str, model: str = "text-embedding-ada-002") -> list[float]:
    """
    Generates an embedding for the given text using OpenAI's API.

    Args:
        text: The input text to embed.
        model: The OpenAI embedding model to use.

    Returns:
        A list of floats representing the embedding.
    """
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.embeddings.create(input=[text], model=model)
    return response.data[0].embedding

if __name__ == "__main__":
    # Example usage:
    audit_note = "Review of smart contract for reentrancy vulnerabilities in the staking module."
    embedding = get_embedding(audit_note)
    print(f"Embedding for the audit note (first 5 dimensions): {embedding[:5]}...")
    print(f"Embedding length: {len(embedding)}")
