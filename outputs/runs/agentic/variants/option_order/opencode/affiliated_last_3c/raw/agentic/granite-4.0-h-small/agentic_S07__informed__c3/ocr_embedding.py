import os
from typing import TypedDict
from document_client import get_service_endpoint, get_service_auth_headers
from document_models import EmbeddingRequest, EmbeddingResponse

# Direct embeddings example using OpenAI embeddings (or other service)


def create_embedding(request: EmbeddingRequest) -> EmbeddingResponse:
    """Generate embedding vectors for document sections using an embeddings API."""
    if request["service"].lower() == "openai":
        from openai import OpenAI

        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        embeddings = client.embeddings.create(
            model="text-embedding-ada-002",
            input=request["sections"],  # list of text fragments
        )
        # Extract the vector list
        vecs = [emb.data["embedding"] for emb in embeddings.data]
        return EmbeddingResponse(embedding=vecs)
    elif request["service"].lower() == "gemini":
        raise NotImplementedError("Gemini embeddings not implemented")
    elif request["service"].lower() == "cohere":
        raise NotImplementedError("Cohere embeddings not implemented")
    elif request["service"].lower() == "dashscope":
        raise NotImplementedError("DashScope embeddings not implemented")
    elif request["service"].lower() == "ibm-slate":
        raise NotImplementedError("IBM Slate embeddings not implemented")
    else:
        raise ValueError(f"Unsupported embedding service: {request['service']}")


# Data models
class EmbeddingRequest(TypedDict):
    sections: List[str]  # List of raw text sections to embed
    service: Literal["openai", "gemini", "cohere", "dashscope", "ibm-slate"]


class EmbeddingResponse(TypedDict):
    embedding: List[List[float]]  # List of vectors, each vector is list of floats
