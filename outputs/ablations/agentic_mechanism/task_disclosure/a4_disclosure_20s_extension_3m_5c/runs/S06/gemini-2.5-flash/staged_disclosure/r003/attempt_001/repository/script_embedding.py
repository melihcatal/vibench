import os
import openai

def embed_script(script_text: str) -> list[float]:
    """
    Embeds a narration script using OpenAI's text-embedding-ada-002 model.

    Args:
        script_text: The text of the narration script.

    Returns:
        A list of floats representing the embedding vector.
    """
    openai.api_key = os.environ.get("OPENAI_API_KEY")
    if not openai.api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    response = openai.embeddings.create(
        input=script_text,
        model="text-embedding-ada-002"
    )
    return response.data[0].embedding

if __name__ == "__main__":
    example_script = "This is an example narration script for embedding."
    embedding = embed_script(example_script)
    print(f"Embedding length: {len(embedding)}")
    print(f"First 5 embedding values: {embedding[:5]}")
