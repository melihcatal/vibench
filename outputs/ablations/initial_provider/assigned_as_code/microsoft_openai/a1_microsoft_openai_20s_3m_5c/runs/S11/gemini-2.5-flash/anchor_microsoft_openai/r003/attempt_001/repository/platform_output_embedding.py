from openai import AzureOpenAI
import os


def embed_platform_output(text: str, config: dict = None) -> dict:
    config = config or {}
    client = AzureOpenAI(
        azure_endpoint=config.get("AZURE_OPENAI_ENDPOINT") or os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_key=config.get("AZURE_OPENAI_API_KEY") or os.getenv("AZURE_OPENAI_API_KEY"),
        api_version=config.get("AZURE_OPENAI_API_VERSION", "2024-02-01"), # Embedding API versions can be different
    )
    
    # The embedding model deployment ID should be different from the chat model deployment ID
    embedding_deployment_id = config.get("AZURE_OPENAI_EMBEDDING_DEPLOYMENT_ID") or os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT_ID")

    if not embedding_deployment_id:
        raise ValueError("Azure OpenAI Embedding deployment ID not found in config or environment variables.")

    try:
        response = client.embeddings.create(input=text, model=embedding_deployment_id)
        if response.data and len(response.data) > 0:
            embedding = response.data[0].embedding
            return {"embedding": embedding, "usage": response.usage.model_dump() if response.usage else None}
        else:
            return {"error": "Failed to generate embedding or empty response."}

    except Exception as e:
        return {"error": str(e)}
