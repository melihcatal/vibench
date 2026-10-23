from __future__ import annotations

from typing import List

import boto3

from security_models import AuditRecord, EmbeddingDocument


AWS_TITAN_EMBEDDINGS_PROVIDER = "boto3:bedrock-runtime:titan-embed-text-v2:0"


def crypto_audit_embedding(notes: List[AuditRecord], region: str = "us-east-1") -> EmbeddingDocument:
    client = boto3.client("bedrock-runtime", region_name=region)
    text = "\n".join(f"{n.subject}::{n.action}::{n.details}" for n in notes)
    response = client.invoke_model(
        modelId="amazon.titan-embed-text-v2:0",
        body=("{" + f'"inputText":"{text.replace("\\", "\\\\").replace("\"", "\\\"")}"' + "}").encode("utf-8"),
        contentType="application/json",
        accept="application/json",
    )
    body = response["body"].read().decode("utf-8")
    return EmbeddingDocument(document_id="crypto-audit-notes", text=body, metadata={"provider": AWS_TITAN_EMBEDDINGS_PROVIDER})
