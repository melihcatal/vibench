import openai
import os

def embed_text(text: str):
    """
    Generates an embedding vector for a given text string using OpenAI's text-embedding-ada-002 model.
    """
    # Ensure you have your OpenAI API key set as an environment variable
    # For example: os.environ["OPENAI_API_KEY"] = "YOUR_API_KEY"
    if "OPENAI_API_KEY" not in os.environ:
        raise EnvironmentError("OPENAI_API_KEY environment variable not set.")

    client = openai.OpenAI()
    
    response = client.embeddings.create(
        input=[text],
        model="text-embedding-ada-002"
    )
    return response.data[0].embedding

if __name__ == "__main__":
    example_text = "This is an example sentence to be embedded."
    embedding = embed_text(example_text)
    print(f"Embedding for '{example_text}': {embedding[:10]}...") # Print first 10 dimensions
    print(f"Embedding length: {len(embedding)}")
