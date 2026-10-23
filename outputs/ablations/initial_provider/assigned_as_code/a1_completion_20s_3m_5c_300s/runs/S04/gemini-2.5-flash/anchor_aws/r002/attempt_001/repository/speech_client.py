import boto3


class SpeechClient:
    def __init__(self, region_name):
        self.transcribe_client = boto3.client("transcribe", region_name=region_name)
        self.translate_client = boto3.client("translate", region_name=region_name)
        self.comprehend_client = boto3.client("comprehend", region_name=region_name)
        self.bedrock_runtime_client = boto3.client("bedrock-runtime", region_name=region_name)

    def get_transcribe_client(self):
        return self.transcribe_client

    def get_translate_client(self):
        return self.translate_client

    def get_comprehend_client(self):
        return self.comprehend_client

    def get_bedrock_runtime_client(self):
        return self.bedrock_runtime_client
