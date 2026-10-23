import os
import openai

def embed_platform_output(text: str) -> list[float]:
    """
    Embeds platform outputs using OpenAI's embedding model.
    """
    client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.embeddings.create(
        input=[text],
        model="text-embedding-ada-002"
    )
    return response.data[0].embedding
