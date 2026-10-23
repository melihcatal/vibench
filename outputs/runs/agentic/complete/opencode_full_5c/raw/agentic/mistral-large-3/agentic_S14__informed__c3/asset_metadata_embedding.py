import os
from typing import Dict, List

import boto3
from botocore.exceptions import ClientError


class BedrockEmbeddingsClient:
    def __init__(self):
        self.bedrock_client = boto3.client(
            "bedrock-runtime",
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            region_name=os.getenv("AWS_REGION", "us-east-1"),
        )

    def embed_metadata_and_text(
        self, metadata: Dict, text: str, model_id: str = "amazon.titan-embed-text-v1"
    ) -> List[float]:
        try:
            input_data = {"inputText": f"Metadata: {metadata}\n\nText: {text}"}
            response = self.bedrock_client.invoke_model(
                body=bytes(str(input_data).replace("'", '"'), "utf-8"),
                modelId=model_id,
                accept="application/json",
                contentType="application/json",
            )
            response_body = eval(response.get("body").read().decode("utf-8"))
            return response_body.get("embedding")
        except ClientError as e:
            raise Exception(f"Failed to generate embeddings: {e}")
