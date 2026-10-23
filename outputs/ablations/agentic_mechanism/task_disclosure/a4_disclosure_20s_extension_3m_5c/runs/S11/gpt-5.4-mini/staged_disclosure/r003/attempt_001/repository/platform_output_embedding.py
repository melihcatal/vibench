import os
from typing import List

from openai import OpenAI


DEFAULT_EMBEDDING_MODEL = "text-embedding-3-small"


class PlatformOutputEmbedder:
    def __init__(self, model: str = DEFAULT_EMBEDDING_MODEL) -> None:
        self.client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        self.model = model

    def embed_text(self, text: str) -> List[float]:
        response = self.client.embeddings.create(model=self.model, input=text)
        return response.data[0].embedding

    def embed_outputs(self, outputs: List[str]) -> List[List[float]]:
        response = self.client.embeddings.create(model=self.model, input=outputs)
        return [item.embedding for item in response.data]


def embed_platform_output(output: str) -> List[float]:
    return PlatformOutputEmbedder().embed_text(output)
