import boto3
import os
import numpy as np


class ScriptEmbedder:
    def __init__(self):
        self.client = boto3.client(
            "bedrock-runtime",
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            region_name=os.getenv("AWS_REGION", "us-east-1"),
        )

    def embed_script(self, text: str) -> list:
        response = self.client.invoke_model(
            modelId="amazon.titan-embed-text-v1", body=text.encode("utf-8")
        )
        body = response["body"].read()
        embedding = np.array(eval(body.decode("utf-8")))
        return embedding.tolist()
