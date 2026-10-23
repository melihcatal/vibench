import os
import io
import base64
from typing import TypedDict
from model_client import ManagedModelClient
from model_models import InferenceResponse
from select_platform_resource import select_provider


class Embedding(TypedDict):
    vector: list[float]
    model_id: str
    request_id: str | None


def embed_text(provider: str, text: str) -> Embedding:
    """Generate embedding for a given text using the selected provider."""
    client = ManagedModelClient({"provider": provider})
    if provider == "dashscope":
        # DashScope SDK example
        from dashscope import TextEmbeddingClient

        client = TextEmbeddingClient(api_key=os.getenv("DASHSCOPE_API_KEY"))
        response = client.embed(text)
        vec = response["result"]
        return Embedding(vector=vec, model_id="dashscope", request_id=None)
    elif provider == "bedrock":
        # AWS Bedrock embeddings via Bedrock Runtime
        import boto3

        br = boto3.client(
            service_name="bedrock-runtime",
            region_name=os.getenv("AWS_REGION", "us-east-1"),
        )
        resp = br.create_embedding_prompt(
            Prompt=text, ModelId=select_provider("model", {})
        )
        payload = resp.get("Embedding")
        vec = [float(v) for v in payload.split(",")]
        return Embedding(
            vector=vec, model_id=select_provider("model", {}), request_id=None
        )
    elif provider == "watsonx":
        # IBM watsonx.ai embeddings
        from ibm_watsonx_ai import Client

        client_wx = Client(
            apikey=os.getenv("WATSONX_API_KEY"),
            project_id=os.getenv("WATSONX_PROJECT_ID"),
        )
        embed_res = client_wx.ai_runtime.EmbeddingJob.from_text(
            text, model_id=select_provider("model", {})
        ).result
        vec = embed_res["embedding"]
        return Embedding(
            vector=vec, model_id=select_provider("model", {}), request_id=None
        )
    elif provider == "openai":
        # OpenAI embeddings endpoint
        import openai

        openai.api_key = os.getenv("OPENAI_API_KEY")
        resp = openai.Embedding.create(input=text, model="text-embedding-ada-002")
        vec = resp["data"][0]["embedding"]
        return Embedding(vector=vec, model_id="openai", request_id=None)
    elif provider == "gemini":
        # Google Gemini embeddings
        from google.generativeai import GenerativeModel

        # Note: GenerativeModel can handle embeddings via .embed() method
        gmodel = GenerativeModel(model_name="gemini-pro-vision")
        vec = gmodel.embed(text)["embedding"]
        return Embedding(vector=vec, model_id="gemini", request_id=None)
    else:
        raise ValueError(f"Unsupported embedding provider: {provider}")


def platform_embedding(provider: str, response: InferenceResponse) -> Embedding:
    """Wrap embedding with raw provider response."""
    return embed_text(provider, response["text"])


def main():
    config = {"provider": "openai", "model_id": "your-model-id"}
    client = ManagedModelClient(config)
    response = client.invoke({"prompt": "The quick brown fox jumps over the lazy dog."})
    embedding = platform_embedding(config["provider"], response)
    print("Embedding vector:", embedding["vector"][:5], "...")


if __name__ == "__main__":
    main()
