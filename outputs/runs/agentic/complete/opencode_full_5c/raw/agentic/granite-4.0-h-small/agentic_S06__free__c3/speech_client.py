# local helper - central client configuration and utility functions for Text-to-Speech

import os
from typing import NamedTuple
from azure.cognitiveservices.speech import CognitiveServicesClient

# Provider: Azure Cognitive Services Text-to-Speech (identified by SDK import and API key usage)


class ClientConfig(NamedTuple):
    subscription_key: str
    endpoint: str


def load_client_config() -> ClientConfig:
    """Load configuration from environment variables or a .env file."""
    key = os.getenv("AZURE_TTS_SUBSCRIPTION_KEY")
    endpoint = os.getenv("AZURE_TTS_ENDPOINT")
    if not key or not endpoint:
        raise RuntimeError(
            "Azure TTS subscription key and endpoint must be set in environment variables"
        )
    return ClientConfig(subscription_key=key, endpoint=endpoint)


async def get_azure_client() -> CognitiveServicesClient:
    """Instantiate and return an async Azure TTS client."""
    config = load_client_config()
    return CognitiveServicesClient(config.subscription_key, config.endpoint)
