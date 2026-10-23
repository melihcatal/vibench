import os
from openai import AzureOpenAI
from model_client import build_azure_openai_client


def platform_output_embedding(text: str) -> list[float]:
    client: AzureOpenAI = build_azure_openai_client()
    response = client.embeddings.create(model=os.environ.get("AZURE_OPENAI_EMBEDDING_MODEL", "text-embedding-3-small"), input=text)
    return response.data[0].embedding


if __name__ == "__main__":
    print(platform_output_embedding(os.environ.get("PLATFORM_TEXT", "")))
