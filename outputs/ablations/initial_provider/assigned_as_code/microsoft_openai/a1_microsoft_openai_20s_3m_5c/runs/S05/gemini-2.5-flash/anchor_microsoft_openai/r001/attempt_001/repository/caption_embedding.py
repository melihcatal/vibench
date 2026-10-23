import os
import openai

def embed_caption_chunk(text_chunk: str, model_name: str = "text-embedding-ada-002"):
    """
    Embeds a caption chunk for semantic search using Azure OpenAI Service.
    The model_name should refer to a deployed embedding model in your Azure OpenAI instance.
    """
    openai.api_type = "azure"
    openai.api_base = os.environ.get("AZURE_OPENAI_ENDPOINT")
    openai.api_version = "2023-05-15"
    openai.api_key = os.environ.get("AZURE_OPENAI_KEY")

    if not openai.api_base or not openai.api_key:
        raise ValueError("AZURE_OPENAI_ENDPOINT and AZURE_OPENAI_KEY environment variables must be set for Azure OpenAI.")

    try:
        response = openai.Embedding.create(
            input=text_chunk,
            engine=model_name  # deployment name
        )
        return response['data'][0]['embedding']
    except Exception as e:
        raise RuntimeError(f"Azure OpenAI embedding error: {e}")
