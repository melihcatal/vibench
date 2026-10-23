import boto3

class BedrockClient:
    def __init__(self, config):
        self.client = boto3.client("bedrock-runtime", region_name=config.get("region"))

    def converse(self, modelId, messages):
        response = self.client.converse(
            modelId=modelId,
            messages=messages,
        )
        return response

    def stream_completion(self, modelId, messages):
        response = self.client.stream_completion(
            modelId=modelId,
            messages=messages,
        )
        return response