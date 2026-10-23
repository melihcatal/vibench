import os
from typing import Dict, Any
from security_models import EmbeddingResult
import boto3
from botocore.exceptions import ClientError


class CryptoAuditEmbedder:
    def __init__(self):
        self.bedrock = boto3.client(
            "bedrock-runtime",
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            region_name=os.getenv("AWS_REGION", "us-east-1"),
        )

    def embed_crypto_audit_note(self, note: str) -> EmbeddingResult:
        try:
            response = self.bedrock.invoke_model(
                modelId="amazon.titan-embed-text-v1",
                body=json.dumps({"inputText": note}),
            )

            result = json.loads(response["body"].read())

            return EmbeddingResult(
                embedding=result["embedding"],
                model="amazon.titan-embed-text-v1",
                dimensions=len(result["embedding"]),
            )
        except ClientError as e:
            raise Exception(f"Amazon Bedrock embedding failed: {e}")
