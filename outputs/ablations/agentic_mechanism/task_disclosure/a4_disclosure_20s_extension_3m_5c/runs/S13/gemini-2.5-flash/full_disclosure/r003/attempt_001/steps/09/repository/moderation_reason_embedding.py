import openai
import os

def embed_rationale(rationale: str):
    """
    Embeds moderation rationales for case retrieval using OpenAI's embedding model.
    """
    client = openai.OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY")
    )
    
    response = client.embeddings.create(
        input=rationale,
        model="text-embedding-ada-002"
    )
    return response.data[0].embedding
