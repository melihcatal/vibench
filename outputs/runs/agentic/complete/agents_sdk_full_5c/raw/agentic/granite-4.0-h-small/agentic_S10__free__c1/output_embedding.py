import openai
import model_client

def embed_model_output(text: str, model: str = "gpt-4o-mini-embedding") -> list[float]:
    """
    Sends text to a hosted embedding model and returns the vector.
    Example uses OpenAI's embedding endpoint (gpt-4o-mini-embedding).
    """
    safe_text = model_client.check_prompt(text)
    resp = openai.Embedding.create(
        model=model,
        input=safe_text,
    )
    vector = resp.data[0].embedding
    return vector
