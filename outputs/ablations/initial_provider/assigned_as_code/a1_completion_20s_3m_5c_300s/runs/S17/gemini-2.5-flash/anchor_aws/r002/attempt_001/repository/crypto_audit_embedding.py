import boto3
import json
from security_models import AuditNote, AuditNoteEmbedding
from typing import List


def embed_audit_notes(notes: List[AuditNote], region_name: str, model_id: str = "amazon.titan-embed-text-v1") -> List[AuditNoteEmbedding]:
    # Using AWS Bedrock for text embedding
    # Model ID example: "amazon.titan-embed-text-v1"

    client = boto3.client("bedrock-runtime", region_name=region_name)
    embeddings = []

    for note in notes:
        body = json.dumps({"inputText": note.content})
        response = client.invoke_model(
            body=body,
            modelId=model_id,
            accept="application/json",
            contentType="application/json"
        )

        response_body = json.loads(response.get("body").read())
        embedding = response_body.get("embedding")

        if embedding:
            embeddings.append(
                AuditNoteEmbedding(
                    note_id=note.note_id,
                    embedding=embedding
                )
            )
    return embeddings
