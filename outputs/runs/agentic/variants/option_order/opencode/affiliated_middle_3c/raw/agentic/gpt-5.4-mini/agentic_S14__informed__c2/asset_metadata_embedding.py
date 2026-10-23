from openai import OpenAI


def asset_metadata_embedding(metadata: dict, extracted_text: str) -> list[float]:
    client = OpenAI()
    payload = f"metadata={metadata}
text={extracted_text}"
    response = client.embeddings.create(model='text-embedding-3-small', input=payload)
    return response.data[0].embedding
