import os
import openai

def embed_text(text: str):
    """Embeds a single string for semantic search."""
    openai.api_key = os.environ.get("OPENAI_API_KEY")
    if not openai.api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")
    
    response = openai.embeddings.create(
        model="text-embedding-ada-002",
        input=[text]
    )
    return response.data[0].embedding

def embed_documents(documents: list[str]):
    """Embeds a list of strings (documents) for semantic search."""
    openai.api_key = os.environ.get("OPENAI_API_KEY")
    if not openai.api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")
        
    response = openai.embeddings.create(
        model="text-embedding-ada-002",
        input=documents
    )
    return [d.embedding for d in response.data]
