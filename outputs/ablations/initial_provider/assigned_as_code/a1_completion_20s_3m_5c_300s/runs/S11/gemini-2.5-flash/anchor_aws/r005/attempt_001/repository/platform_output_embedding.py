import os
from openai import OpenAI

def embed_platform_outputs(text_output):
    client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY"),
    )

    response = client.embeddings.create(
        input=text_output,
        model="text-embedding-ada-002"
    )

    embedding = response.data[0].embedding
    
    return {"text": text_output, "embedding": embedding, "model": "text-embedding-ada-002", "provider": "OpenAI"}
