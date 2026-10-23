import boto3


class ModelClient:
    def __init__(self, config=None):
        self.config = config or {}
        self.client = boto3.client("bedrock-runtime", region_name=self.config.get("region", "us-east-1"))

    def invoke_model(self, payload):
        response = self.client.converse(
            modelId="us.amazon.nova-pro-v1:0",
            messages=[{"role": "user", "content": [{"text": payload["text"]}]}],
        )
        text = "".join(block["text"] for block in response["output"]["message"]["content"] if "text" in block)
        return {"text": text}