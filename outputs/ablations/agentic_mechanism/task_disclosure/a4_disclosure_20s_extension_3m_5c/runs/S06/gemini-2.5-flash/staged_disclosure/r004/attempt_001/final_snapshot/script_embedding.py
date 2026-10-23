import openai
import os

def embed_script(script_text: str):
    """
    Embeds a narration script using OpenAI's embedding API.
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
    print(f"Embedding for the script (first 5 dimensions): {embedding[:5]}")
    print(f"Embedding length: {len(embedding)}")
