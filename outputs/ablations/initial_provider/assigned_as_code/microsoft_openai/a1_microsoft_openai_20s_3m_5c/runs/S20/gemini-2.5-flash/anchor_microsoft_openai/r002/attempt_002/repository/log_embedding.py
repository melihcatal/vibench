import os
from openai import AzureOpenAI
from observability_models import EmbeddingRequest

def log_embedding(request: EmbeddingRequest) -> dict:
    azure_openai_endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT")
    azure_openai_key = os.environ.get("AZURE_OPENAI_KEY")
    azure_openai_embedding_deployment_name = os.environ.get("AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME")

    if not all([azure_openai_endpoint, azure_openai_key, azure_openai_embedding_deployment_name]):
        raise ValueError("Missing Azure OpenAI embedding environment variables: AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_KEY, AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME")

    client = AzureOpenAI(
        azure_endpoint=azure_openai_endpoint,
        api_key=azure_openai_key,
        api_version="2024-02-01", # Or your specific API version
    )

    response = client.embeddings.create(
        model=azure_openai_embedding_deployment_name, # deployment name
        input=[request.text]
    )

    embedding = response.data[0].embedding
    return {"embedding": embedding}
