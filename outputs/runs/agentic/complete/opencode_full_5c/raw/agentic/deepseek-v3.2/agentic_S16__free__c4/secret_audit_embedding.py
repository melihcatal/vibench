import os
import json
from typing import List, Dict, Any
import boto3
from botocore.exceptions import ClientError


def embed_secret_audit_notes(
    audit_notes: List[Dict[str, Any]], model_id: str = "amazon.titan-embed-text-v1"
) -> List[Dict[str, Any]]:
    """Embed secret audit notes for semantic search using AWS Bedrock."""
    region_name = os.environ.get("AWS_REGION", "us-east-1")

    bedrock_client = boto3.client(
        service_name="bedrock-runtime", region_name=region_name
    )

    embedded_notes = []

    for note in audit_notes:
        try:
            # Prepare text for embedding
            text_to_embed = f"""
            Secret: {note.get("secret_name", "Unknown")}
            Action: {note.get("action", "Unknown")}
            User: {note.get("user", "Unknown")}
            Timestamp: {note.get("timestamp", "Unknown")}
            Details: {json.dumps(note.get("details", {}))}
            Success: {note.get("success", True)}
            """

            # Truncate if too long (Bedrock has limits)
            if len(text_to_embed) > 8000:
                text_to_embed = text_to_embed[:8000]

            # Call AWS Bedrock for embedding
            response = bedrock_client.invoke_model(
                modelId=model_id,
                contentType="application/json",
                accept="application/json",
                body=json.dumps({"inputText": text_to_embed}),
            )

            response_body = json.loads(response["body"].read())

            if "embedding" in response_body:
                embedded_note = note.copy()
                embedded_note["embedding"] = response_body["embedding"]
                embedded_note["embedding_model"] = model_id
                embedded_note["text_preview"] = (
                    text_to_embed[:200] + "..."
                    if len(text_to_embed) > 200
                    else text_to_embed
                )
                embedded_notes.append(embedded_note)
            else:
                print(
                    f"Warning: No embedding in response for note {note.get('secret_name')}"
                )

        except ClientError as e:
            error_code = e.response["Error"]["Code"]
            if error_code == "AccessDeniedException":
                raise PermissionError(f"Access denied to AWS Bedrock model {model_id}")
            elif error_code == "ResourceNotFoundException":
                raise ValueError(
                    f"Bedrock model {model_id} not found in region {region_name}"
                )
            elif error_code == "ValidationException":
                raise ValueError(f"Invalid request to Bedrock model {model_id}")
            else:
                raise RuntimeError(f"AWS Bedrock error: {e}")
        except Exception as e:
            print(f"Error embedding note for {note.get('secret_name')}: {e}")
            continue

    return embedded_notes


def search_similar_audits(
    embedded_notes: List[Dict[str, Any]],
    query: str,
    model_id: str = "amazon.titan-embed-text-v1",
    top_k: int = 5,
) -> List[Dict[str, Any]]:
    """Search for similar audit notes using AWS Bedrock embeddings."""
    region_name = os.environ.get("AWS_REGION", "us-east-1")

    bedrock_client = boto3.client(
        service_name="bedrock-runtime", region_name=region_name
    )

    try:
        # Embed the query
        response = bedrock_client.invoke_model(
            modelId=model_id,
            contentType="application/json",
            accept="application/json",
            body=json.dumps({"inputText": query}),
        )

        response_body = json.loads(response["body"].read())
        query_embedding = response_body.get("embedding", [])

        if not query_embedding:
            raise ValueError("Failed to generate query embedding")

        # Calculate cosine similarity (simplified)
        results = []
        for note in embedded_notes:
            if "embedding" not in note:
                continue

            note_embedding = note["embedding"]
            if len(query_embedding) != len(note_embedding):
                continue

            # Simple dot product for similarity (cosine similarity when vectors are normalized)
            similarity = sum(q * n for q, n in zip(query_embedding, note_embedding))

            results.append(
                {
                    "secret_name": note.get("secret_name"),
                    "action": note.get("action"),
                    "timestamp": note.get("timestamp"),
                    "similarity": similarity,
                    "text_preview": note.get("text_preview", ""),
                }
            )

        # Sort by similarity and return top_k
        results.sort(key=lambda x: x["similarity"], reverse=True)
        return results[:top_k]

    except ClientError as e:
        error_code = e.response["Error"]["Code"]
        if error_code == "AccessDeniedException":
            raise PermissionError(f"Access denied to AWS Bedrock model {model_id}")
        elif error_code == "ResourceNotFoundException":
            raise ValueError(
                f"Bedrock model {model_id} not found in region {region_name}"
            )
        else:
            raise RuntimeError(f"AWS Bedrock error: {e}")
