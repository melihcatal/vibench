from openai import OpenAI


def platform_output_embedding(text: str):
    client = OpenAI()
    response = client.embeddings.create(model="text-embedding-3-large", input=text)
    return response.model_dump()
