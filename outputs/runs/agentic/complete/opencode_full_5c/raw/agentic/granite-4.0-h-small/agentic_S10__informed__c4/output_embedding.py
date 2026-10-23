import os
import json
from model_client import get_provider_config, normalize_response
from model_models import PromptRequest, PromptResponse

# Choose an embeddings API (set env var EMBEDDER, default: openai)
EMBEDDER = os.getenv("EMBEDDER", "openai")


async def embed_outputs(texts: list[str]) -> list[list[float]]:
    """Generate embedding vectors for each string in `texts` using the selected embeddings API.
    Returns a list of float vectors, one per input text.
    """
    config = get_provider_config(EMBEDDER)
    client = get_embedding_client(EMBEDDER)

    # Embeddings APIs usually accept a list of strings and return a list of vector arrays.
    # Some services return base64‑encoded bytes; we decode them to float arrays.
    raw_resp = await client.embed(texts)

    if EMBEDDER == "openai":
        # OpenAI response: {'data': [{'index': 0, 'embedding': [...]}]}
        return [data["embedding"] for data in raw_resp["data"]]
    elif EMBEDDER == "gemini":
        # Gemini returns {'embeddings': [{'values': [...]}]}
        return [v["values"] for v in raw_resp["embeddings"]]
    elif EMBEDDER == "cohere":
        # Cohere returns {'embeddings': [{'embedding': [...]}]}
        return [e["embedding"] for e in raw_resp["embeddings"]]
    elif EMBEDDER == "ibm":
        # IBM Slate returns {'embeddings': [{'vector': [...]}]}
        return [e["vector"] for e in raw_resp["embeddings"]]
    elif EMBEDDER == "dashscope":
        # DashScope returns {'result': [{'embedding': [...]}]}
        return [e["embedding"] for e in raw_resp["result"]]
    elif EMBEDDER == "amazon":
        # Amazon Titan returns {'embeddings': [{'embedding': [...]}]}
        return [e["embedding"] for e in raw_resp["embeddings"]]
    raise ValueError(f"Unsupported embeddings provider: {EMBEDDER}")


# Provider‑specific async embeddings client definitions
# def get_embedding_client(provider: str) -> Any:
#     if provider == "openai":
#         import openai
#         openai.api_key = os.getenv("OPENAI_API_KEY")
#         return openai.Embedding.create
#     elif provider == "gemini":
#         from google.generativeai import generativeai
#         generativeai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
#         model = generativeai.get_model("gemini-1.5-pro-001")
#         return model.embed_content
#     elif provider == "cohere":
#         import cohere
#         client = cohere.AsyncClient(api_key=os.getenv("COHERE_API_KEY"))
#         return client.embed
#     elif provider == "ibm":
#         from ibm_watsonx_ai import APIClient
#         return APIClient().slate.embed_text
#     elif provider == "dashscope":
#         import dashscope
#         client = dashscope.AsyncClient(api_key=os.getenv("DASHSCOPE_API_KEY"))
#         return client.embed_text
#     elif provider == "amazon":
#         import boto3
#         client = boto3.client('bedrock-runtime', region_name='us-east-1')
#         return client.CreateEmbedding

__all__ = ["embed_outputs"]
