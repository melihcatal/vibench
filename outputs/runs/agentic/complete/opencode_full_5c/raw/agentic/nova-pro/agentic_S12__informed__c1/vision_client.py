import os
from dashscope import Vision


class VisionClient:
    def __init__(self):
        self.api_key = os.getenv("DASHSCOPE_API_KEY")
        self.client = Vision(api_key=self.api_key)

    def get_client(self):
        return self.client
