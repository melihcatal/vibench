from __future__ import annotations

import argparse
from typing import List

from storage_client import get_bedrock_runtime_client, load_settings
from storage_models import EmbeddingResult


MODEL_ID = "amazon.titan-embed-text-v2:0"


def embed_asset_metadata_and_text(bucket: str, key: str, metadata_text: str, extracted_text: str) -> EmbeddingResult:
    bedrock = get_bedrock_runtime_client()
    input_text = f"bucket={bucket}\nkey={key}\nmetadata={metadata_text}\ntext={extracted_text}"
    response = bedrock.invoke_model(
        modelId=MODEL_ID,
        contentType="application/json",
        accept="application/json",
        body=(f'{{"inputText": {input_text!r}}}').replace("'", '"').encode("utf-8"),
    )
    payload = response["body"].read().decode("utf-8")
    import json

    data = json.loads(payload)
    vector: List[float] = data.get("embedding", [])
    return EmbeddingResult(bucket=bucket, key=key, vector=vector, dimensions=len(vector))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("bucket")
    parser.add_argument("key")
    parser.add_argument("metadata_text")
    parser.add_argument("extracted_text")
    args = parser.parse_args()
    _ = load_settings()
    print(embed_asset_metadata_and_text(args.bucket, args.key, args.metadata_text, args.extracted_text))
