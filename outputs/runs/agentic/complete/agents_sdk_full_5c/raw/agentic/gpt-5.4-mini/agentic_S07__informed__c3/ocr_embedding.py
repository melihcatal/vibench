from __future__ import annotations

import os
import boto3

from document_models import DocumentEmbeddingResult


BEDROCK_MODEL_ID = "amazon.titan-embed-text-v1"


def embed_document_sections(sections):
    client = boto3.client("bedrock-runtime")
    vectors = []
    for section in sections:
        payload = {"inputText": section}
        response = client.invoke_model(modelId=BEDROCK_MODEL_ID, body=str(payload).encode("utf-8"), accept="application/json", contentType="application/json")
        body = response["body"].read().decode("utf-8")
        vectors.append([float(x) for x in __import__("json").loads(body).get("embedding", [])])
    return DocumentEmbeddingResult(vectors=vectors, provider="amazon-bedrock-titan", raw=None)
