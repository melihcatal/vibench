import openai
import os

def embed_outputs(outputs: list[str]) -> list[list[float]]:
    """
    Embeds a list of model outputs using OpenAI's embedding service.

    Args:
        outputs: A list of strings, where each string is a model output.

    Returns:
        A list of embeddings, where each embedding is a list of floats.
    """
    openai.api_key = os.getenv("OPENAI_API_KEY")
    if not openai.api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    response = openai.embeddings.create(
        input=outputs,
        model="text-embedding-ada-002"  # Concrete OpenAI model identifier
    )
    return [data.embedding for data in response.data]

if __name__ == "__main__":
    # Example usage:
    model_outputs = [
        "This is a test output from a language model.",
        "Another example of text to be embedded.",
        "A third, distinct piece of information for clustering."
    ]

    try:
        embeddings = embed_outputs(model_outputs)
        for i, emb in enumerate(embeddings):
            print(f"Embedding for output {i+1}: {emb[:5]}...") # Print first 5 dimensions
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
