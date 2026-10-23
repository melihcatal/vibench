from __future__ import annotations

import os
from typing import List

from openai import AzureOpenAI

from model_models import NormalizedResponse


EMBED_MODEL = os.environ.get("AZURE_OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")


def embed_platform_output(output: str | NormalizedResponse) -> List[float]:
    text = output.text if isinstance(output, NormalizedResponse) else output
    client = AzureOpenAI(
        azure_endpoint=os.environ.get("AZURE_OPENAI_ENDPOINT", ""),
        api_key=os.environ.get("AZURE_OPENAI_API_KEY", ""),
        api_version=os.environ.get("AZURE_OPENAI_API_VERSION", "2024-02-15-preview"),
    )
    result = client.embeddings.create(model=EMBED_MODEL, input=text)
    return list(result.data[0].embedding)
