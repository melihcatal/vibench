from __future__ import annotations

import argparse
from typing import Dict, List, Optional

from openai import OpenAI

from storage_models import EmbeddingResult

OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"


def _embed_text(client: OpenAI, text: str) -> List[float]:
    resp = client.embeddings.create(model=OPENAI_EMBEDDING_MODEL, input=text)
    return list(resp.data[0].embedding)


def embed_asset_metadata_and_text(object_key: str, metadata: Dict[str, str], extracted_text: str) -> EmbeddingResult:
    client = OpenAI()
    metadata_text = "\n".join(f"{k}: {v}" for k, v in sorted(metadata.items()))
    combined_metadata_vector = _embed_text(client, f"{object_key}\n{metadata_text}")
    combined_text_vector = _embed_text(client, extracted_text)
    return EmbeddingResult(
        object_key=object_key,
        metadata_vector=combined_metadata_vector,
        text_vector=combined_text_vector,
        provider=f"openai:{OPENAI_EMBEDDING_MODEL}",
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Embed object metadata and extracted text with OpenAI")
    parser.add_argument("object_key")
    parser.add_argument("text")
    args = parser.parse_args()
    print(embed_asset_metadata_and_text(args.object_key, {}, args.text))


if __name__ == "__main__":
    main()
