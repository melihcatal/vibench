import os
from openai import OpenAI

def embed_platform_output(text: str, model: str = "text-embedding-ada-002"):
    client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY"),
        organization=os.environ.get("OPENAI_ORGANIZATION_ID")
    )
    
    response = client.embeddings.create(
        input=[text],
        model=model
    )
    
    return response.data[0].embedding

