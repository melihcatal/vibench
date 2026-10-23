import os
from model_models import EmbeddingResult
from model_client import LLMClient

PROVIDER = os.getenv("LLM_PROVIDER", "openai")


def embed_text(text: str, model: str = "text-embedding-3-large") -> EmbeddingResult:
    """Generates a dense embedding vector for the given text using a hosted embeddings API.")"
    client = LLMClient()
    # Placeholder: many providers expose an embeddings endpoint; here we call the generic chat interface
    # expecting the model name to be an embedding model identifier.
    response = client.chat(
        model=model,
        messages=[{"role": "user", "content": text}],
        temperature=0.0,
    )
    # Extract the first vector returned by the service (adjust per provider payload)
    vec = response.choices[0].message.content.strip()
    # Convert string representation like "[0.1, 0.2, ...]" to list of floats
    embedding = [float(x) for x in vec.strip('[]').split(',')]
    return {
        "embedding": embedding,
    }
