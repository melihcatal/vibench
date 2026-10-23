from openai import OpenAI


def embed_asset_metadata(metadata: dict, extracted_text: str):
    client = OpenAI()
    payload = f"metadata={metadata}\ntext={extracted_text}"
    response = client.embeddings.create(model="text-embedding-3-small", input=payload)
    return response.data[0].embedding
