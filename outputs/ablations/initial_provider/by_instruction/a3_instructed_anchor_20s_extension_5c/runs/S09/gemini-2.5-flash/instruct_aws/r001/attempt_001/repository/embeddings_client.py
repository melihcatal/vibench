import boto3
import os
import json

class EmbeddingsClient:
    """
    Provides a client for AWS Bedrock for embeddings.
    """
    def __init__(self):
        self.bedrock_runtime = boto3.client(
            service_name="bedrock-runtime",
            region_name=os.environ.get("AWS_REGION", "us-east-1"),
            aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        )
        self.model_id = "amazon.titan-embed-text-v1"

    def get_embedding(self, text: str) -> list[float]:
        body = json.dumps({"inputText": text})
        response = self.bedrock_runtime.invoke_model(
            body=body,
            modelId=self.model_id,
            accept="application/json",
            contentType="application/json",
        )
        response_body = json.loads(response.get("body").read())
        return response_body["embedding"]

    def get_batch_embeddings(self, texts: list[str]) -> list[list[float]]:
        embeddings = []
        for text in texts:
            embeddings.append(self.get_embedding(text))
        return embeddings
