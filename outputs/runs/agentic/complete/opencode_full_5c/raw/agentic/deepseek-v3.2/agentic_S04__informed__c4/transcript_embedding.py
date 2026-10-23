import os
import json
from typing import List, Dict, Any
import boto3
from botocore.exceptions import ClientError
import numpy as np


def embed_transcript_segments(segments: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    bedrock_client = boto3.client(
        "bedrock-runtime",
        region_name=os.getenv("AWS_REGION", "us-east-1"),
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    )

    embedded_segments = []

    for segment in segments:
        text = segment.get("text", "")
        if not text.strip():
            embedded_segments.append(
                {**segment, "embedding": [], "embedding_dimension": 0}
            )
            continue

        try:
            body = json.dumps({"inputText": text})

            response = bedrock_client.invoke_model(
                modelId="amazon.titan-embed-text-v2:0",
                body=body,
                contentType="application/json",
            )

            response_body = json.loads(response["body"].read())
            embedding = response_body.get("embedding", [])

            embedded_segments.append(
                {
                    **segment,
                    "embedding": embedding,
                    "embedding_dimension": len(embedding),
                    "model_used": "amazon.titan-embed-text-v2:0",
                }
            )

        except ClientError as e:
            print(f"Error embedding segment: {e}")
            embedded_segments.append(
                {**segment, "embedding": [], "embedding_dimension": 0, "error": str(e)}
            )

    return embedded_segments


def embed_transcript_text(text: str) -> Dict[str, Any]:
    bedrock_client = boto3.client(
        "bedrock-runtime",
        region_name=os.getenv("AWS_REGION", "us-east-1"),
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    )

    try:
        body = json.dumps({"inputText": text})

        response = bedrock_client.invoke_model(
            modelId="amazon.titan-embed-text-v2:0",
            body=body,
            contentType="application/json",
        )

        response_body = json.loads(response["body"].read())
        embedding = response_body.get("embedding", [])

        return {
            "text": text,
            "embedding": embedding,
            "embedding_dimension": len(embedding),
            "model_used": "amazon.titan-embed-text-v2:0",
        }

    except ClientError as e:
        raise RuntimeError(f"Failed to embed text: {e}")


def batch_embed_segments(
    segments: List[Dict[str, Any]], batch_size: int = 5
) -> List[Dict[str, Any]]:
    bedrock_client = boto3.client(
        "bedrock-runtime",
        region_name=os.getenv("AWS_REGION", "us-east-1"),
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    )

    all_embedded_segments = []

    for i in range(0, len(segments), batch_size):
        batch = segments[i : i + batch_size]
        batch_texts = [s.get("text", "") for s in batch]

        try:
            body = json.dumps({"inputTexts": batch_texts})

            response = bedrock_client.invoke_model(
                modelId="amazon.titan-embed-text-v2:0",
                body=body,
                contentType="application/json",
            )

            response_body = json.loads(response["body"].read())
            embeddings = response_body.get("embeddings", [])

            for j, (segment, embedding) in enumerate(zip(batch, embeddings)):
                all_embedded_segments.append(
                    {
                        **segment,
                        "embedding": embedding,
                        "embedding_dimension": len(embedding),
                        "model_used": "amazon.titan-embed-text-v2:0",
                        "batch_index": i + j,
                    }
                )

        except ClientError as e:
            print(f"Error embedding batch {i}: {e}")
            for segment in batch:
                all_embedded_segments.append(
                    {
                        **segment,
                        "embedding": [],
                        "embedding_dimension": 0,
                        "error": str(e),
                    }
                )

    return all_embedded_segments


def semantic_search(
    embedded_segments: List[Dict[str, Any]], query: str, top_k: int = 3
) -> List[Dict[str, Any]]:
    bedrock_client = boto3.client(
        "bedrock-runtime",
        region_name=os.getenv("AWS_REGION", "us-east-1"),
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    )

    try:
        query_body = json.dumps({"inputText": query})

        query_response = bedrock_client.invoke_model(
            modelId="amazon.titan-embed-text-v2:0",
            body=query_body,
            contentType="application/json",
        )

        query_response_body = json.loads(query_response["body"].read())
        query_embedding = np.array(query_response_body.get("embedding", []))

        if len(query_embedding) == 0:
            return []

        scored_segments = []

        for segment in embedded_segments:
            segment_embedding = segment.get("embedding", [])
            if not segment_embedding or len(segment_embedding) != len(query_embedding):
                continue

            segment_vec = np.array(segment_embedding)
            similarity = np.dot(query_embedding, segment_vec) / (
                np.linalg.norm(query_embedding) * np.linalg.norm(segment_vec)
            )

            scored_segments.append({**segment, "similarity_score": float(similarity)})

        scored_segments.sort(key=lambda x: x["similarity_score"], reverse=True)

        return scored_segments[:top_k]

    except ClientError as e:
        print(f"Error in semantic search: {e}")
        return []


def cluster_transcript_segments(
    embedded_segments: List[Dict[str, Any]], n_clusters: int = 3
) -> List[Dict[str, Any]]:
    from sklearn.cluster import KMeans

    valid_segments = [
        s
        for s in embedded_segments
        if s.get("embedding") and len(s.get("embedding", [])) > 0
    ]

    if not valid_segments:
        return []

    embeddings = np.array([s["embedding"] for s in valid_segments])

    if len(embeddings) < n_clusters:
        n_clusters = len(embeddings)

    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    cluster_labels = kmeans.fit_predict(embeddings)

    clustered_segments = []
    for segment, label in zip(valid_segments, cluster_labels):
        clustered_segments.append(
            {
                **segment,
                "cluster_id": int(label),
                "cluster_center_distance": float(
                    np.linalg.norm(
                        segment["embedding"] - kmeans.cluster_centers_[label]
                    )
                ),
            }
        )

    return clustered_segments
