import openai
import os

def embed_script(script_text: str):
    """
    Embeds narration scripts using OpenAI's embedding model for voice-asset search.
    """
    client = openai.OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY")
    )
    response = client.embeddings.create(
        input=script_text,
        model="text-embedding-ada-002"  # Concrete OpenAI model identifier
    )
    return response.data[0].embedding
