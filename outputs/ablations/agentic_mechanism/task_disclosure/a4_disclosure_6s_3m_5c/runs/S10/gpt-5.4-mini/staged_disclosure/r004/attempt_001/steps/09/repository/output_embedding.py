import os
from typing import List, Sequence

from openai import OpenAI


class OutputEmbedder:
    def __init__(self, api_key: str | None = None, model: str = "text-embedding-3-small") -> None:
        self.client = OpenAI(api_key=api_key or os.environ.get("OPENAI_API_KEY"))
        self.model = model

    def embed_text(self, text: str) -> List[float]:
        response = self.client.embeddings.create(model=self.model, input=text)
        return list(response.data[0].embedding)

    def embed_outputs(self, outputs: Sequence[str]) -> List[List[float]]:
        response = self.client.embeddings.create(model=self.model, input=list(outputs))
        return [list(item.embedding) for item in response.data]


def embed_for_clustering(outputs: Sequence[str], api_key: str | None = None) -> List[List[float]]:
    return OutputEmbedder(api_key=api_key).embed_outputs(outputs)


def embed_for_retrieval(query: str, api_key: str | None = None) -> List[float]:
    return OutputEmbedder(api_key=api_key).embed_text(query)
