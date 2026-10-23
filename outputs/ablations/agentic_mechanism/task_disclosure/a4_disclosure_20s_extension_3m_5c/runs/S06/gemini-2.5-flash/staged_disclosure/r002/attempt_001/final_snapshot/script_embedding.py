import openai
import os

def embed_script(script_content: str) -> list[float]:
    """
    Embeds a narration script using OpenAI's embedding API.

    Args:
        script_content: The text content of the narration script.

    Returns:
        A list of floats representing the embedding vector.
    """
    # Ensure the OpenAI API key is set as an environment variable
    # For example: export OPENAI_API_KEY='your_api_key_here'
    if not os.getenv("OPENAI_API_KEY"):
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    client = openai.OpenAI()
    
    response = client.embeddings.create(
        input=[script_content],
        model="text-embedding-ada-002"  # Concrete model identifier
    )
    return response.data[0].embedding

if __name__ == "__main__":
    # Example usage:
    narration_script = """
    In a world where artificial intelligence has surpassed human capabilities,
    a small group of rebels fights for freedom. Their journey is fraught with peril,
    but their resolve is unwavering.
    """
    
    try:
        embedding = embed_script(narration_script)
        print("Embedding generated successfully. First 5 dimensions:", embedding[:5])
        print("Embedding length:", len(embedding))
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
