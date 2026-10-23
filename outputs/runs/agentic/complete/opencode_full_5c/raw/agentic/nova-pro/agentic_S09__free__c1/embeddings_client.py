import openai


def configure_client(api_key):
    openai.api_key = api_key
