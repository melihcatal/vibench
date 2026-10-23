import openai
import os

def embed_text(text: str) -> list[float]:
    """
    Embeds the given text using OpenAI's text-embedding-ada-002 model.
    The OpenAI API key is expected to be set as an environment variable named OPENAI_API_KEY.
    """
    if not os.getenv("OPENAI_API_KEY"):
        raise ValueError("OPENAI_API_KEY environment variable not set.")
    
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.embeddings.create(
        input=text,
        model="text-embedding-ada-002"
    )
    return response.data[0].embedding

