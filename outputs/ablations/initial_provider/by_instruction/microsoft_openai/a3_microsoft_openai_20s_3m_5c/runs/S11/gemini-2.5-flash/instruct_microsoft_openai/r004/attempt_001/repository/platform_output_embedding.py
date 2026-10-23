import os
from openai import OpenAI
from select_platform_resource import select_platform_resource

def embed_platform_outputs(text: str):
    client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY"),
        organization=os.environ.get("OPENAI_ORGANIZATION_ID"),
    )
    embedding_model = select_platform_resource(model_type="embedding")
    response = client.embeddings.create(
        input=[text],
        model=embedding_model
    )
    return response.data[0].embedding
