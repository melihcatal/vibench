import os
import json
from model_client import ManagedModelClient
from model_models import ModelInvocationResponse


# Azure OpenAI Embeddings endpoint – reuse same endpoint/keys
class PlatformOutputEmbedding:
    """
    Generate embeddings for model output using Azure OpenAI Embeddings API.
    Returns vector and usage metadata.
    """

    def create_embedding(self, text: str) -> dict:
        from openai import OpenAI

        client = OpenAI(
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            api_base=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_type="azure",
        )
        resp = client.embeddings.create(model="text-embedding-ada-002", input=text)
        return {"embedding": resp.data[0].embedding, "finish_reason": None, "index": 0}

    def embed_response(self, response: ModelInvocationResponse) -> dict:
        # Use first choice content as example text
        text = response.choices[0]["message"]["content"]
        return self.create_embedding(text)
