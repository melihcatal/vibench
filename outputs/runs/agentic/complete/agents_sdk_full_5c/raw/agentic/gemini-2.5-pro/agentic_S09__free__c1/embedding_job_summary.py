from typing import List, Dict
from embeddings_client import get_openai_client

def summarize_embedding_batch(texts: List[str]) -> Dict:
    """
    Processes a batch of texts to generate embeddings using OpenAI and returns
    a summary of the API usage.

    Args:
        texts: A list of text strings to embed.

    Returns:
        A dictionary summarizing the embedding job results.
    """
    openai_client = get_openai_client()
    
    response = openai_client.embeddings.create(
        input=texts,
        model="text-embedding-3-small"  # Using a specific OpenAI model
    )
    
    usage = response.usage
    
    summary = {
        "model": response.model,
        "texts_processed": len(response.data),
        "total_tokens": usage.total_tokens,
        "prompt_tokens": usage.prompt_tokens,
    }
    
    return summary
