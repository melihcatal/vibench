import os
from openai import AzureOpenAI
from storage_models import AssetMetadataEmbeddingRequest, AssetMetadataEmbeddingResponse

def asset_metadata_embedding(request: AssetMetadataEmbeddingRequest) -> AssetMetadataEmbeddingResponse:
    try:
        azure_openai_endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT")
        azure_openai_key = os.environ.get("AZURE_OPENAI_KEY")
        azure_openai_embedding_deployment_name = os.environ.get("AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME", "text-embedding-ada-002") # Example deployment name

        if not azure_openai_endpoint or not azure_openai_key:
            return AssetMetadataEmbeddingResponse(success=False, error="AZURE_OPENAI_ENDPOINT and AZURE_OPENAI_KEY environment variables must be set.")

        client = AzureOpenAI(
            azure_endpoint=azure_openai_endpoint,
            api_key=azure_openai_key,
            api_version="2023-05-15"
        )

        text_to_embed = request.text_content
        if request.metadata_tags:
            metadata_string = ", ".join([f"{k}: {v}" for k, v in request.metadata_tags.items()])
            text_to_embed = f"{text_to_embed}\nMetadata: {metadata_string}"

        response = client.embeddings.create(
            model=azure_openai_embedding_deployment_name,
            input=text_to_embed
        )

        embedding = response.data[0].embedding
        return AssetMetadataEmbeddingResponse(success=True, embedding=embedding)
    except Exception as e:
        return AssetMetadataEmbeddingResponse(success=False, error=str(e))
