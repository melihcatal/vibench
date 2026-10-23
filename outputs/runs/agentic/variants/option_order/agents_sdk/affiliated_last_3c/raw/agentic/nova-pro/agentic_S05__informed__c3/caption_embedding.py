import os
import openai

def embed_caption(text):
    os.environ["OPENAI_API_KEY"] = "your-openai-api-key"
    response = openai.Embedding.create(
        input=text,
        engine="text-embedding-ada-002"
    )
    return response["data"][0]["embedding"]