import os
import json
import boto3
from botocore.exceptions import ClientError
from security_models import AuditEmbeddingRequest, AuditEmbeddingResponse
from security_client import get_bedrock_client


def embed_audit_notes(audit_notes, model_id="amazon.titan-embed-text-v2:0"):
    request = AuditEmbeddingRequest(
        audit_notes=audit_notes,
        model_id=model_id,
    )
    client = get_bedrock_client()
    try:
        body = json.dumps(
            {
                "inputText": request.audit_notes,
                "dimensions": 1024,
                "normalize": True,
            }
        )
        response = client.invoke_model(
            modelId=request.model_id,
            body=body,
        )
        response_body = json.loads(response["body"].read())
        embedding = response_body.get("embedding", [])
        input_tokens = response_body.get("inputTextTokenCount", 0)
        return AuditEmbeddingResponse(
            embedding=embedding,
            model_id=request.model_id,
            input_tokens=input_tokens,
        )
    except ClientError as e:
        raise RuntimeError(
            f"Audit note embedding failed: {e.response['Error']['Message']}"
        ) from e
