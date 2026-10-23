import openai
import os

def embed_moderation_rationale(rationale_text: str, model: str = "text-embedding-ada-002") -> list[float]:
    """
    Generates an embedding for the given moderation rationale text using OpenAI's embedding API.
    """
    client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    response = client.embeddings.create(
        input=[rationale_text],
        model=model
    )
    
    # The response contains a list of embeddings, we expect one for a single input text
    if response.data:
        return response.data[0].embedding
    return []
