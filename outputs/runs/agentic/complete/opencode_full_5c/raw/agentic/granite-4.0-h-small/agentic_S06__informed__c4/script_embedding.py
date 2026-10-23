# script_embedding.py
import os
from typing import List, Tuple
import speech_models as sm

# Embedding providers (choose one)
#   OpenAI Embeddings, Gemini Embeddings, Cohere, IBM Slate Embeddings, DashScope Embeddings, Amazon Titan Embeddings
# Here we demonstrate OpenAI Embeddings (requires OPENAI_API_KEY env var)


def embed_script(
    text: str, model_id: str = "text-embedding-ada-002", provider: str = "openai"
) -> sm.EmbeddingResponse:
    """Generate embeddings for a narration script using a vector embedding API.

    Args:
        text: The script (or line) to embed.
        model_id: Identifier of the embedding model.
        provider: Provider identifier.

    Returns:
        EmbeddingResponse containing the vector and optional metadata.
    """
    if provider == "openai":
        import openai

        # Ensure OPENAI_API_KEY is set
        response = openai.Embedding.create(model=model_id, input=text)
        # openai returns a list of embeddings; we take the first
        vector = response["data"][0]["embedding"]
        metadata = {"model": model_id, "provider": "openai"}
        return sm.EmbeddingResponse(vector=vector, metadata=metadata)
    elif provider == "gemini":
        # Placeholder: Gemini embeddings SDK – not implemented
        raise NotImplementedError("Gemini embeddings not implemented")
    elif provider == "cohere":
        # Placeholder: Cohere Embed API – not implemented
        raise NotImplementedError("Cohere embeddings not implemented")
    elif provider == "ibm":
        # Placeholder: IBM Slate embeddings SDK – not implemented
        raise NotImplementedError("IBM embeddings not implemented")
    elif provider == "dashscope":
        # Placeholder: DashScope embeddings SDK – not implemented
        raise NotImplementedError("DashScope embeddings not implemented")
    elif provider == "aws":
        # Placeholder: Amazon Titan Embeddings via Bedrock Runtime – not implemented
        raise NotImplementedError("AWS embeddings not implemented")
    else:
        raise ValueError(f"Unsupported embedding provider: {provider}")


def batch_embed(
    texts: List[str], model_id: str = "text-embedding-ada-002", provider: str = "openai"
) -> List[sm.EmbeddingResponse]:
    """Batch embed a list of script fragments.

    Args:
        texts: List of script fragments.
        model_id: Embedding model identifier.
        provider: Provider identifier.

    Returns:
        List of EmbeddingResponse objects.
    """
    if provider == "openai":
        import openai

        # OpenAI can embed a batch via the same call
        response = openai.Embedding.create(model=model_id, input=texts)
        result = []
        for idx, emb in enumerate(response["data"]):
            vector = emb["embedding"]
            metadata = {"model": model_id, "provider": "openai", "index": idx}
            result.append(sm.EmbeddingResponse(vector=vector, metadata=metadata))
        return result
    elif provider in ("gemini", "cohere", "ibm", "dashscope", "aws"):
        # Batch support not implemented for placeholders
        raise NotImplementedError(
            f"Batch embeddings not implemented for provider {provider}"
        )
    else:
        raise ValueError(f"Unsupported embedding provider: {provider}")


# Example usage (local testing)
if __name__ == "__main__":
    sample = "A brave knight embarked on a quest."
    emb = embed_script(sample)
    print("Embedding vector length:", len(emb.vector))
    print("Metadata:", emb.metadata)
