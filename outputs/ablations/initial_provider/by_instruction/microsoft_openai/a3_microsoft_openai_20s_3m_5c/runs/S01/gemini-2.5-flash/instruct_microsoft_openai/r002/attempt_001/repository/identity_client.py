import os
from openai import OpenAI

class IdentityClient:
    def __init__(self):
        self.openai_client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    def get_openai_client(self):
        return self.openai_client
