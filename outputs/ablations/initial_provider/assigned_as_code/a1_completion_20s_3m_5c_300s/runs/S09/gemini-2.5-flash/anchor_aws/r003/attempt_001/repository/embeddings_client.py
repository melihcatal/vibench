import boto3
import json
import os

class BedrockEmbeddingsClient:
    def __init__(self, region_name=None, model_id="amazon.titan-embed-text-v2:0"):
        self.region_name = region_name or os.environ.get("AWS_REGION", "us-east-1")
        self.model_id = model_id
        self.client = boto3.client("bedrock-runtime", region_name=self.region_name)

    def invoke_model(self, text_input):
        body = json.dumps({"inputText": text_input})
        response = self.client.invoke_model(
            modelId=self.model_id,
            body=body,
            contentType="application/json",
            accept="application/json"
        )
        stream = response["body"]
        try:
            return json.loads(stream.read())
        finally:
            stream.close()

    def invoke_model_batch(self, text_inputs):
        # Bedrock's invoke_model doesn't directly support batch.
        # This is a conceptual helper for batching on the client side.
        embeddings = []
        for text in text_inputs:
            result = self.invoke_model(text)
            embeddings.append(result.get("embedding"))
        return {"embeddings": embeddings}
