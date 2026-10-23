import os
import cohere
from model_models import ModelConfig
from dotenv import load_dotenv

load_dotenv()


class ModelClient:
    def __init__(self):
        config = ModelConfig(api_key=os.getenv("COHERE_API_KEY"))
        if not config.api_key:
            raise ValueError("COHERE_API_KEY environment variable not set.")
        self.client = cohere.Client(config.api_key)

    def get_client(self):
        return self.client


_client_instance = None


def get_model_client():
    global _client_instance
    if _client_instance is None:
        _client_instance = ModelClient()
    return _client_instance.get_client()
