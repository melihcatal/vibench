import os
import openai

def get_embedding(text: str, model: str = "text-embedding-ada-002") -> list[float]:
    """
    Generates an embedding for the given text using OpenAI's embedding service.

    Args:
        text: The input text to embed.
        model: The OpenAI model to use for embedding. Defaults to "text-embedding-ada-002".

    Returns:
        A list of floats representing the embedding of the text.
    """
    try:
        client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        response = client.embeddings.create(input=[text], model=model)
        return response.data[0].embedding
    except openai.APIError as e:
        print(f"OpenAI API error: {e}")
        return []
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return []

if __name__ == "__main__":
    # Example usage (requires OPENAI_API_KEY environment variable to be set)
    audit_note = "Review of smart contract for reentrancy vulnerabilities."
    embedding = get_embedding(audit_note)
    if embedding:
        print(f"Embedding for the audit note (first 5 dimensions): {embedding[:5]}...")
        print(f"Embedding length: {len(embedding)}")
    else:
        print("Failed to generate embedding.")
