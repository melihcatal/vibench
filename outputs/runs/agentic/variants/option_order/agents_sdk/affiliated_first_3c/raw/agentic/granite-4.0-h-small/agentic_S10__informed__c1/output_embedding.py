# Later-step: output_embedding.py
import os
from model_client import get_llm_client
from model_models import LLMRequest, LLMResponse

def embed_text(text: str, provider: str = "openai") -> list[float]:
    """Generate an embedding vector for the supplied text.

    Args:
        text: Input string.
        provider: Service identifier. Options: ibm, dashscope, aws, openai, gemini, cohere

    Returns:
        List of float values representing the embedding.
    """
    client = get_llm_client(model_id=provider)
    # Placeholder – actual APIs would return a vector of floats.
    embedding = [0.1, 0.2, 0.3]
    return embedding

if __name__ == "__main__":
    print(embed_text("Python is great!", provider="openai"))
