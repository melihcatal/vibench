import os
import openai

def get_embedding(text: str, model: str = "text-embedding-ada-002") -> list[float]:
    """
    Generates an embedding for the given text using OpenAI's embedding API.

    Args:
        text: The input text to embed.
        model: The OpenAI embedding model to use.

    Returns:
        A list of floats representing the embedding of the text.
    """
    openai.api_key = os.getenv("OPENAI_API_KEY")
    if not openai.api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    try:
        response = openai.embeddings.create(input=text, model=model)
        return response.data[0].embedding
    except openai.APIError as e:
        print(f"OpenAI API error: {e}")
        raise

if __name__ == "__main__":
    audit_note = "This audit reviewed the smart contract for potential reentrancy vulnerabilities."
    try:
        embedding = get_embedding(audit_note)
        print(f"Embedding generated (first 5 dimensions): {embedding[:5]}...")
        print(f"Embedding length: {len(embedding)}")
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
