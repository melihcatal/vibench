import os
import google.generativeai as genai

class EmbeddingsClient:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.environ.get("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY not found. Please set the environment variable or pass it to the client.")
        genai.configure(api_key=self.api_key)

    def get_client(self):
        return genai
