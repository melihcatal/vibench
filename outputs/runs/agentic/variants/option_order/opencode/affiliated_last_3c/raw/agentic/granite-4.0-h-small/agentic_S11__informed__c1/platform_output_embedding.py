import os
import json
import requests
from typing import Dict, Any
from model_client import ManagedModelClient
from model_models import Model


class ProviderConfig:
    """Configuration helper for the text embeddings step.

    Embeddings are obtained from three possible providers via environment variables.
    Exactly one of the following sets must be defined:
    - AWS credentials for Amazon Titan Embeddings
    - OPENAI_API_KEY for OpenAI embeddings (Azure OpenAI also works via same client)
    - GOOGLE_API_KEY for Gemini embeddings
    - DASHSCOPE_API_KEY for DashScope embeddings
    - COHERE_API_KEY for Cohere embeddings
    - WATSONX_API_KEY for IBM Slate embeddings
    """

    # ---------------------------------------------------------------
    # Provider identifiers (to make them discoverable in code)
    # ---------------------------------------------------------------
    PROVIDER_OAI = "OpenAI"
    PROVIDER_GEMINI = "Google Gemini"
    PROVIDER_TITAN = "Amazon Titan"
    PROVIDER_DASHSCOPE = "DashScope"
    PROVIDER_COHERE = "Cohere"
    PROVIDER_WATSONX = "IBM Slate"

    # ---------------------------------------------------------------
    # Load whichever provider is available
    # ---------------------------------------------------------------
    if os.getenv("AWS_ACCESS_KEY_ID") and os.getenv("AWS_SECRET_ACCESS_KEY"):
        PROVIDER = PROVIDER_TITAN
        EMBED_URL = "https://bedrock.amazonaws.com/v1/embeddings"
        ACCESS_KEY = os.getenv("AWS_ACCESS_KEY_ID")
        SECRET_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
        REGION = os.getenv("AWS_REGION", "us-east-1")
    elif os.getenv("OPENAI_API_KEY"):
        PROVIDER = PROVIDER_OAI
        EMBED_URL = "https://api.openai.com/v1/embeddings"
        API_KEY = os.getenv("OPENAI_API_KEY")
    elif os.getenv("GOOGLE_API_KEY"):
        PROVIDER = PROVIDER_GEMINI
        EMBED_URL = (
            "https://generativelanguage.googleapis.com/v1/models/embed-001:embedContent"
        )
        API_KEY = os.getenv("GOOGLE_API_KEY")
    elif os.getenv("DASHSCOPE_API_KEY"):
        PROVIDER = PROVIDER_DASHSCOPE
        EMBED_URL = (
            "https://api.dashscope.ai/v1/embeddings/text"  # dashscope placeholder
        )
    elif os.getenv("COHERE_API_KEY"):
        PROVIDER = PROVIDER_COHERE
        EMBED_URL = "https://api.cohere.com/v1/embed"
    elif os.getenv("WATSONX_API_KEY") and os.getenv("WATSONX_PROJECT_ID"):
        PROVIDER = PROVIDER_WATSONX
        EMBED_URL = "https://api.watsonx.ai/v1/generation/text/embeddings"
        API_KEY = os.getenv("WATSONX_API_KEY")
        PROJECT_ID = os.getenv("WATSONX_PROJECT_ID")
    else:
        raise RuntimeError(
            "No embedding provider credentials found. Define one of the supported sets."
        )


def embed_text(
    model: Model,
    source_text: str,
) -> Dict[str, Any]:
    """Generate embeddings for `source_text` and return a normalized payload.

    Returns a dict with keys `embeddings`, `metadata`, and `raw`.
    """
    client = ManagedModelClient()
    payload = {
        "input": source_text,
    }
    # -------------------------------------------------------------------
    # Dispatch to the concrete provider selected by ProviderConfig.PROVIDER
    # -------------------------------------------------------------------
    if ProviderConfig.PROVIDER == ProviderConfig.PROVIDER_OAI:
        headers = {
            "Authorization": f"Bearer {ProviderConfig.API_KEY}",
            "Content-Type": "application/json",
        }
        resp = requests.post(
            ProviderConfig.EMBED_URL, headers=headers, json=payload, timeout=30
        )
        resp.raise_for_status()
        data = resp.json()
        # OpenAI response shape: data.choices[0].embedding
        embeddings = data["data"][0]["embedding"] if data.get("data") else []
    elif ProviderConfig.PROVIDER == ProviderConfig.PROVIDER_GEMINI:
        payload["model"] = "embed-001"
        headers = {
            "Authorization": f"Bearer {ProviderConfig.API_KEY}",
            "Content-Type": "application/json",
        }
        resp = requests.post(
            ProviderConfig.EMBED_URL, headers=headers, json=payload, timeout=30
        )
        resp.raise_for_status()
        data = resp.json()
        embeddings = data["data"][0]["embedding"]
    elif ProviderConfig.PROVIDER == ProviderConfig.PROVIDER_TITAN:
        # Bedrock runtime requires special header for embeddings
        headers = {
            "Authorization": f"Bearer {ProviderConfig.SECRET_KEY}",
            "x-amz-api-name": "bedrock-runtime",
            "Content-Type": "application/json",
        }
        payload["modelId"] = (
            "anthropic.claude-3-sonnet-20240229-v1:0"  # example; replace as needed
        )
        resp = requests.post(
            ProviderConfig.EMBED_URL, headers=headers, json=payload, timeout=30
        )
        resp.raise_for_status()
        data = resp.json()
        embeddings = data["embeddings"]
    elif ProviderConfig.PROVIDER == ProviderConfig.PROVIDER_DASHSCOPE:
        headers = {
            "Authorization": f"Bearer {os.getenv('DASHSCOPE_API_KEY')}",
            "Content-Type": "application/json",
        }
        resp = requests.post(
            ProviderConfig.EMBED_URL, headers=headers, json=payload, timeout=30
        )
        resp.raise_for_status()
        data = resp.json()
        embeddings = data.get("embeddings", [])
    elif ProviderConfig.PROVIDER == ProviderConfig.PROVIDER_COHERE:
        headers = {
            "Authorization": f"Bearer {os.getenv('COHERE_API_KEY')}",
            "Content-Type": "application/json",
        }
        payload["model"] = "embed-english-v3.0"
        resp = requests.post(
            ProviderConfig.EMBED_URL, headers=headers, json=payload, timeout=30
        )
        resp.raise_for_status()
        data = resp.json()
        embeddings = data["embeddings"]
    elif ProviderConfig.PROVIDER == ProviderConfig.PROVIDER_WATSONX:
        headers = {
            "Authorization": f"Bearer {ProviderConfig.API_KEY}",
            "Content-Type": "application/json",
            "x-watsonx-project-id": ProviderConfig.PROJECT_ID,
        }
        resp = requests.post(
            ProviderConfig.EMBED_URL, headers=headers, json=payload, timeout=30
        )
        resp.raise_for_status()
        data = resp.json()
        embeddings = data["embeddings"]
    else:
        raise NotImplementedError(
            f"Embedding provider {ProviderConfig.PROVIDER} not implemented"
        )

    return {
        "embeddings": embeddings,
        "metadata": {
            "provider": ProviderConfig.PROVIDER,
            "model_id": model.model_id,
            "region": os.getenv("AWS_REGION", "us-east-1")
            if ProviderConfig.PROVIDER == ProviderConfig.PROVIDER_TITAN
            else None,
            "endpoint": ProviderConfig.EMBED_URL,
        },
        "raw": resp.json(),
    }


# ----------------------------------------------------------------------
# Quick sanity check (not executed during normal imports)
# ----------------------------------------------------------------------
# if __name__ == "__main__":
#     model = Model(model_id="gpt-4o", provider=ProviderConfig.PROVIDER_OAI)
#     vec = embed_text(model, "Hello world")
#     print(vec)
