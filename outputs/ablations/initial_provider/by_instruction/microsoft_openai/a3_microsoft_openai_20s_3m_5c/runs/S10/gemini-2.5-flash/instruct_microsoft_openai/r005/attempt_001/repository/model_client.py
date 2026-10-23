import os
from openai import OpenAI

class OpenAIClient:
    """
    Provides a configured OpenAI client.
    """
    def __init__(self):
        self._client = OpenAI(
            api_key=os.environ.get("OPENAI_API_KEY"),
            organization=os.environ.get("OPENAI_ORGANIZATION"),
        )

    @property
    def client(self) -> OpenAI:
        return self._client

def get_openai_client() -> OpenAI:
    return OpenAIClient().client
