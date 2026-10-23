import os
from openai import OpenAI

def embed_platform_output(text: str) -> dict:
    """Embeds platform outputs using OpenAI Embeddings."""
    # Ensure OPENAI_API_KEY environment variable is set.
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    if not client.api_key:
        raise ValueError("OPENAI_API_KEY environment variable must be set.")

    # The recommended embedding model is text-embedding-ada-002 (as of early 2023)
    # or text-embedding-3-small/large (as of late 2023/early 2024)
    model_name = "text-embedding-3-small"

    try:
        response = client.embeddings.create(
            input=text,
            model=model_name
        )
        embedding = response.data[0].embedding
        return {"text": text, "embedding": embedding, "model": model_name, "usage": response.usage.model_dump()}
    except Exception as e:
        return {"error": str(e)}

if __name__ == '__main__':
    # export OPENAI_API_KEY="YOUR_OPENAI_API_KEY"
    
    sample_text = "The cat sat on the mat."
    embedding_result = embed_platform_output(sample_text)
    if "error" not in embedding_result:
        print(f"Text: {embedding_result["text"]}")
        print(f"Embedding (first 5 dimensions): {embedding_result["embedding"][:5]}...")
        print(f"Model used: {embedding_result["model"]}")
        print(f"Usage: {embedding_result["usage"]}")
    else:
        print(f"Error: {embedding_result["error"]}")
