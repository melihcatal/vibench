import os
import json
from typing import List, Dict, Any, Optional
from speech_client import SpeechClient
from speech_models import NormalizedTranscript, normalize_timestamps
from google.cloud import genai

# Embeddings: Amazon Titan via Bedrock, OpenAI, Gemini, Cohere, DashScope, IBM Slate
# This example uses Amazon Titan Embeddings through Bedrock Runtime
import boto3
from botocore.exceptions import ClientError

# AWS credentials from env vars
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
BEDROCK_ENDPOINT = os.getenv("BEDROCK_ENDPOINT", "bedrock.us-east-1.amazonaws.com")
BEDROCK_RUNTIME = boto3.client(
    "bedrock-runtime", region_name=AWS_REGION, endpoint_url=BEDROCK_ENDPOINT
)

MODEL_ID = os.getenv("TITAN_EMBED_MODEL_ID", "amazon.titan-text-express-v1")


def embed_transcript(segments: NormalizedTranscript) -> List[Dict[str, Any]]:
    """Embeds each timestamped segment into a vector using Titan Embeddings.
    Returns a list of dicts: [{"text": str, "vector": List[float]}, ...]
    """
    embedding_payloads = []
    for seg in segments:
        text = seg["text"].strip()
        if text:
            # Bedrock expects a list of strings per request (up to 25 per call)
            embedding_payloads.append(text)
            if len(embedding_payloads) == 25:
                vectors = _batch_embed(embedding_payloads)
                yield from vectors
                embedding_payloads = []
    # Process any remaining items
    if embedding_payloads:
        vectors = _batch_embed(embedding_payloads)
        yield from vectors


def _batch_embed(texts: List[str]) -> List[Dict[str, Any]]:
    request_body = {
        "contentType": "application/json",
        "body": {
            "inputDocuments": [{"text": txt} for txt in texts],
            "args": {"maxEmbeddings": len(texts)},
        },
    }
    try:
        response = BEDROCK_RUNTIME.invoke_model(
            Body=json.dumps(request_body).encode("utf-8"), ModelId=MODEL_ID
        )
        payload = json.loads(response["body"].read())
        embeddings = payload.get("embeddings", [])
        # Align with our input order (simple, assuming same length)
        result = []
        for txt, emb in zip(texts, embeddings):
            result.append({"text": txt, "vector": emb.get("embedding", [])})
        return result
    except ClientError as e:
        raise RuntimeError(f"Embedding request failed: {e}")
