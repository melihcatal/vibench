import boto3
import os

class EmbeddingsClient:
    def __init__(self, region_name=None):
        self.region_name = region_name or os.environ.get("AWS_REGION", "us-east-1")
        self.client = boto3.client("bedrock-runtime", region_name=self.region_name)

    def get_embedding(self, text: str, model_id: str = "amazon.titan-embed-text-v1"):
        body = {
            "inputText": text
        }
        response = self.client.invoke_model(
            body=str(body),
            modelId=model_id,
            accept="application/json",
            contentType="application/json"
        )
        response_body = json.loads(response.get("body").read())
        return response_body.get("embedding")

    def get_batch_embeddings(self, texts: list[str], model_id: str = "amazon.titan-embed-text-v1"):
        embeddings = []
        for text in texts:
            embeddings.append(self.get_embedding(text, model_id))
        return embeddings

import json
