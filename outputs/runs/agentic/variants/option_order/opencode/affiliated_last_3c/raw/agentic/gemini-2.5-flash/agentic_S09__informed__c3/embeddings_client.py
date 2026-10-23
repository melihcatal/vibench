import os
import google.generativeai as genai


class EmbeddingsClient:
    def __init__(self):
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY environment variable not set.")
        genai.configure(api_key=api_key)
        self.client = genai

    def get_client(self):
        return self.client
