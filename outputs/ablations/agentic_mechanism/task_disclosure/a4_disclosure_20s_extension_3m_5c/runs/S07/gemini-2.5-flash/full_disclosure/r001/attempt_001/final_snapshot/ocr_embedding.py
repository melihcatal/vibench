import openai
import os

def embed_document_section(text: str):
    """
    Embeds extracted document sections for semantic retrieval using OpenAI's embedding API.
    """
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.embeddings.create(
        input=text,
        model="text-embedding-ada-002"
    )
    return response.data[0].embedding
