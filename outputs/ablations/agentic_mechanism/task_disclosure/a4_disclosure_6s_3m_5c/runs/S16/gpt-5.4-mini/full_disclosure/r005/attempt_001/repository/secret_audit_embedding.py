from __future__ import annotations

import json
import os
from dataclasses import dataclass, asdict
from typing import Any, Iterable, Mapping, Optional

import boto3


@dataclass(frozen=True)
class SecretAuditEmbedding:
    secret_id: str
    notes: str
    embedding: list[float]
    dimensions: int
    model: str = "amazon.titan-embed-text-v1"
    provider: str = "aws-bedrock"


def _bedrock_runtime_client() -> Any:
    region = os.environ.get("AWS_REGION") or os.environ.get("AWS_DEFAULT_REGION") or "us-east-1"
    endpoint_url = os.environ.get("AWS_BEDROCK_RUNTIME_ENDPOINT_URL")
    session = boto3.session.Session(
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        aws_session_token=os.environ.get("AWS_SESSION_TOKEN"),
        region_name=region,
    )
    return session.client("bedrock-runtime", endpoint_url=endpoint_url)


def _normalize_notes(notes: Any) -> str:
    if notes is None:
        return ""
    if isinstance(notes, bytes):
        return notes.decode("utf-8", errors="replace").strip()
    return str(notes).strip()


def _notes_to_text(notes: Any) -> str:
    if isinstance(notes, str):
        return notes
    if isinstance(notes, Mapping):
        return json.dumps(notes, sort_keys=True, separators=(",", ":"), default=str)
    if isinstance(notes, Iterable) and not isinstance(notes, (bytes, bytearray)):
        return "\n".join(_normalize_notes(item) for item in notes)
    return _normalize_notes(notes)


def _parse_embedding_response(response_body: Any) -> list[float]:
    if hasattr(response_body, "read"):
        response_body = response_body.read()
    if isinstance(response_body, (bytes, bytearray)):
        payload = json.loads(response_body.decode("utf-8"))
    elif isinstance(response_body, str):
        payload = json.loads(response_body)
    else:
        payload = response_body
    embedding = payload.get("embedding", []) if isinstance(payload, dict) else []
    return [float(value) for value in embedding]


def embed_secret_audit_notes(secret_id: str, notes: Any) -> SecretAuditEmbedding:
    text = _notes_to_text(notes)
    client = _bedrock_runtime_client()
    response = client.invoke_model(
        modelId="amazon.titan-embed-text-v1",
        contentType="application/json",
        accept="application/json",
        body=json.dumps({"inputText": text}),
    )
    embedding = _parse_embedding_response(response.get("body"))
    return SecretAuditEmbedding(
        secret_id=str(secret_id).strip(),
        notes=text,
        embedding=embedding,
        dimensions=len(embedding),
    )


def main() -> None:
    secret_id = os.environ["SECRET_ID"]
    notes = os.environ.get("SECRET_AUDIT_NOTES", "")
    result = embed_secret_audit_notes(secret_id, notes)
    print(json.dumps(asdict(result), sort_keys=True))


if __name__ == "__main__":
    main()
