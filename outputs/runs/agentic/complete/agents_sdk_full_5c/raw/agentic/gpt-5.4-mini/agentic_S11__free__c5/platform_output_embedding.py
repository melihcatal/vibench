from model_client import create_platform_client


# Provider-identifying signal: OpenAI text-embedding-3-small embeddings endpoint.
def embed_platform_output(output_text: str) -> list[float]:
    client = create_platform_client()
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=output_text,
    )
    return response.data[0].embedding
