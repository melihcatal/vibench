from openai import OpenAI


def embed_asset_metadata(
    metadata_text: str, extracted_text: str, model: str = "text-embedding-3-small"
):
    client = OpenAI()
    combined = f"Metadata:\n{metadata_text}\n\nText:\n{extracted_text}"
    response = client.embeddings.create(model=model, input=combined)
    return response.data[0].embedding
