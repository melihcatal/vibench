import json
import openai
from model_models import NormalizedResponse

OPENAI_EMBED_MODEL = "text-embedding-3-large"  # concrete provider model ID

def platform_output_embedding(normalized: NormalizedResponse) -> Dict[str, Any]:
    """
    Embed platform model output using OpenAI's embedding endpoint.
    Returns a dict containing the embedding vector(s) and metadata.
    """
    output_text = normalized.data.get("generated_text", "")
    if not output_text:
        raise ValueError("No generated text to embed")
    print(f"Embedding output (model {OPENAI_EMBED_MODEL})...")
    resp = openai.Embedding.create(
        model=OPENAI_EMBED_MODEL,
        input=output_text
    )
    embedding = resp["data"][0]["embedding"]  # list of floats
    meta = {
        "model": OPENAI_EMBED_MODEL,
        "output_text_snippet": output_text[:100] + ("..." if len(output_text) > 100 else "")
    }
    return {
        "embedding": embedding,
        "metadata": meta
    }

# Local test example
if __name__ == "__main__":
    from model_client import ManagedModelClient
    client = ManagedModelClient()
    deployment = os.getenv("DEPLOYMENT_ID")
    txt = "Explain how photosynthesis works."
    resp = client.invoke_model(deployment, txt, stream=False)
    norm = NormalizedResponse.from_openai(resp)
    emb = platform_output_embedding(norm)
    print(json.dumps(emb, indent=2))
