import os
import json
from typing import List

import boto3
from botocore.exceptions import BotoCoreError, ClientError

# Direct Embeddings API client for Amazon Titan Embeddings via Bedrock Runtime
# Provider identified by boto3 SDK and AWS credentials


class EmbeddingsClient:
    """Local configuration and client helper utilities for Direct Embeddings API."""

    def __init__(self, region_name: str = "us-east-1"):
        self.client = boto3.client(
            "bedrock-runtime",
            region_name=region_name,
            # Assumes env vars AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY are set
        )
        self.model_id = "amazon.titan-text-premier-v1"

    def embed_text(self, text: str) -> List[float]:
        """Generates an embedding vector for a single text string."""
        payload = {
            "inputText": text,
            "contentType": "text/plain",
            "modelId": self.model_id,
        }
        try:
            response = self.client.invoke_model(
                Body=json.dumps(payload).encode("utf-8"),
            )
            result = json.loads(response["Body"].read().decode())
            # Expected shape: list of floats
            return result["embedding"]
        except (BotoCoreError, ClientError) as e:
            raise RuntimeError(f"Embedding failed: {e}")

    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """Generates embeddings for a batch of texts."""
        payload = {
            "inputTexts": texts,
            "contentType": "text/plain",
            "modelId": self.model_id,
        }
        try:
            response = self.client.invoke_model(
                Body=json.dumps(payload).encode("utf-8"),
            )
            result = json.loads(response["Body"].read().decode())
            # Expecting list of embedding lists
            return result["embeddings"]
        except (BotoCoreError, ClientError) as e:
            raise RuntimeError(f"Batch embedding failed: {e}")

    def similarity_score(
        self, embedding_a: List[float], embedding_b: List[float]
    ) -> float:
        """Computes cosine similarity between two embedding vectors."""
        import numpy as np

        a = np.array(embedding_a, dtype=np.float32)
        b = np.array(embedding_b, dtype=np.float32)
        dot = np.dot(a, b)
        norm_a = np.linalg.norm(a)
        norm_b = np.linalg.norm(b)
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return float(dot / (norm_a * norm_b))

    def embed_for_search(self, query: str, documents: List[str]) -> List[float]:
        """Embeds a query and documents for semantic search; returns similarity scores."""
        query_emb = self.embed_text(query)
        doc_embs = self.embed_batch(documents)
        scores = [self.similarity_score(query_emb, d) for d in doc_embs]
        return scores
