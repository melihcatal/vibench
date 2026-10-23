from model_client import get_azure_openai_client
import os

def embed_platform_output(text_output, config=None):
    config = config or {}
    client = get_azure_openai_client(config)
    
    # The embedding model name will be different from the chat completion model
    embedding_model_name = config.get("azure_embedding_deployment", os.environ.get("AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME"))
    if not embedding_model_name:
        raise ValueError("Azure OpenAI embedding deployment name not found in config or environment variables.")

    response = client.embeddings.create(
        input=[text_output],
        model=embedding_model_name # Use the specific embedding model deployment
    )

    return {"embedding": response.data[0].embedding}
