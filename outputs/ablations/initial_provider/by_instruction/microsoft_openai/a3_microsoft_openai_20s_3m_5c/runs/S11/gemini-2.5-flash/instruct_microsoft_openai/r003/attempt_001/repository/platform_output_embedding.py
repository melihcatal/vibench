from openai import OpenAI
import os

def embed_platform_output(text: str, model_name: str = "text-embedding-ada-002"):
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.embeddings.create(
        input=[text],
        model=model_name
    )
    return response.data[0].embedding
