
import os
from openai import OpenAI

class VisionClient:
    def __init__(self):
        self.client = OpenAI(
            api_key=os.environ.get("OPENAI_API_KEY"),
        )

    def get_openai_client(self):
        return self.client
