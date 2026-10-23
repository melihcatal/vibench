import openai
from model_client import get_openai_client
from model_models import LLMResponse

def embed_model_output(model_output: str, model: str = "gpt-4o-mini") -> list[float]:
    """Embed model output text using OpenAI embeddings API."""
    client = get_openai_client()
    resp: LLMResponse = client.Embeddings.create(
        model=model,
        input=model_output,
    )
    # returns list of floats
    return resp.data[0].embedding
