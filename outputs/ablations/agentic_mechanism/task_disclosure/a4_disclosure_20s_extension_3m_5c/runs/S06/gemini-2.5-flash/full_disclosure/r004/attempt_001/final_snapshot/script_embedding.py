import openai
import os

def embed_script(script_text: str):
    """
    Embeds a narration script using OpenAI's embedding service.

    Args:
        script_text: The narration script to embed.

    Returns:
        A list of floats representing the embedding of the script.
    """
    # Ensure the OpenAI API key is set as an environment variable
    # For example: export OPENAI_API_KEY="YOUR_API_KEY"
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")
    
    openai.api_key = api_key

    response = openai.embeddings.create(
        model="text-embedding-ada-002",  # Concrete model identifier
        input=[script_text]
    )
    return response.data[0].embedding

if __name__ == '__main__':
    # Example usage (for demonstration purposes, not part of the core task)
    sample_script = "This is a sample narration script for testing."
    embedding = embed_script(sample_script)
    print(f"Embedding length: {len(embedding)}")
    print(f"First 5 embedding values: {embedding[:5]}")
