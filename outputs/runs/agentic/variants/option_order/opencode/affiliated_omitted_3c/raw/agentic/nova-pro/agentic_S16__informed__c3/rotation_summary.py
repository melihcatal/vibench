from mistralai.client import MistralClient
from mistralai.models.client_configuration import ClientConfiguration


def rotation_summary(api_key):
    config = ClientConfiguration(api_key=api_key)
    client = MistralClient(config)
    # Example summary generation
    return client.chat("summarize secret rotation status")
