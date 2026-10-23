from openai import OpenAI
import os

# Set up the client
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)


def embed_text(text):
    return (
        client.embeddings.create(input=text, model="text-embedding-ada-002")
        .data[0]
        .embedding
    )
