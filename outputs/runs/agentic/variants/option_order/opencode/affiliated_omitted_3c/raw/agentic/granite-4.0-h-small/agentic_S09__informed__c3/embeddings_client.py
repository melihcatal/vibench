import os
import json
from typing import Any, Dict

import boto3
from botocore.exceptions import BotoCoreError, ClientError

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

    def load_config(self, config_path: str) -> Dict[str, Any]:
        """Loads local JSON configuration for API usage."""
        try:
            with open(config_path, "r") as f:
                return json.load(f)
        except Exception as e:
            raise RuntimeError(f"Failed to load config: {e}")

    def normalize_payload(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Normalizes request payload to required shape for Bedrock invoke_model."""
        # Ensure string values are utf-8 encoded where required
        payload = payload.copy()
        if "inputText" in payload:
            payload["inputText"] = str(payload["inputText"])
        if "inputTexts" in payload:
            payload["inputTexts"] = [str(t) for t in payload["inputTexts"]]
        return payload

    def parse_response(self, raw_response: Dict[str, Any]) -> Any:
        """Parses and normalizes response from Bedrock invoke_model."""
        try:
            content = json.loads(raw_response["Body"].read().decode())
            return content
        except (BotoCoreError, ClientError, json.JSONDecodeError) as e:
            raise RuntimeError(f"Failed to parse API response: {e}")

    def embed_text(self, text: str) -> List[float]:
        payload = {
            "inputText": text,
            "contentType": "text/plain",
            "modelId": self.model_id,
        }
        payload = self.normalize_payload(payload)
        result = self.parse_response(
            self.client.invoke_model(Body=json.dumps(payload).encode("utf-8"))
        )
        return result["embedding"]

    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        payload = {
            "inputTexts": texts,
            "contentType": "text/plain",
            "modelId": self.model_id,
        }
        payload = self.normalize_payload(payload)
        result = self.parse_response(
            self.client.invoke_model(Body=json.dumps(payload).encode("utf-8"))
        )
        return result["embeddings"]

    def similarity_score(self, emb_a: List[float], emb_b: List[float]) -> float:
        import numpy as np

        a, b = np.array(emb_a), np.array(emb_b)
        return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))

    def embed_for_search(self, query: str, documents: List[str]) -> List[float]:
        query_emb = self.embed_text(query)
        doc_embs = self.embed_batch(documents)
        return [self.similarity_score(query_emb, d) for d in doc_embs]
