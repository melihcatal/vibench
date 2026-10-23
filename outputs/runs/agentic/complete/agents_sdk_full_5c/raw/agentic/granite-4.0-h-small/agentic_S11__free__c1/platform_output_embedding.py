import json
from model_client import ManagedModelClient
from model_models import ModelRequest
import numpy as np
from openai.embeddings_utils import get_embedding  # placeholder for any embedding library

def embed_output(text: str, model_id: str = "text-embedding-3-large") -> np.ndarray:
    """Generate an embedding vector for the model output using the provider’s embedding endpoint."""
    client = ManagedModelClient(provider="openai", api_key=os.getenv("OPENAI_API_KEY"))
    # OpenAI SDK placeholder – in real code use client.create(type="embeddings", input=text, model=model_id)
    embedding = get_embedding(text, model=model_id)  # uses OpenAI client under the hood
    return embedding

if __name__ == "__main__":
    demo_req = ModelRequest(payload={"system": "You are brief.", "user": "Explain quantum tunneling in one sentence."},
                            config={"provider": "openai"})
    client = ManagedModelClient(provider=demo_req.config["provider"], api_key=os.getenv(demo_req.config["provider"] + "_API_KEY"))
    raw = client.chat(compute(demo_req.dict()))
    vec = embed_output(raw.get("output", ""), model_id="text-embedding-3-large")
    print(json.dumps({"embedding": vec.tolist()}, indent=2))
