from __future__ import annotations

import os

import boto3

from storage_client import normalize_boto_error
from storage_models import dict_to_text, EmbeddingDocument


bedrock = boto3.client("bedrock-runtime", region_name=os.environ.get("AWS_REGION", "us-east-1"))
EMBEDDING_MODEL_ID = os.environ.get("BEDROCK_EMBEDDING_MODEL_ID", "amazon.titan-embed-text-v2:0")


def asset_metadata_embedding(object_key: str, metadata: dict, extracted_text: str) -> dict:
    document = EmbeddingDocument(
        object_key=object_key,
        metadata_text=dict_to_text(metadata),
        extracted_text=extracted_text,
    )
    payload_text = f"Object Key: {document.object_key}\n\nMetadata:\n{document.metadata_text}\n\nExtracted Text:\n{document.extracted_text}"
    try:
        response = bedrock.invoke_model(
            modelId=EMBEDDING_MODEL_ID,
            body=(f'{{"inputText": {payload_text!r}}}').encode("utf-8"),
            accept="application/json",
            contentType="application/json",
        )
        return {"object_key": object_key, "model_id": EMBEDDING_MODEL_ID, "embedding_response": response["body"].read().decode("utf-8")}
    except Exception as exc:
        return {"error": normalize_boto_error(exc), "model_id": EMBEDDING_MODEL_ID}
