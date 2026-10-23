import os
from amazon.bedrock import client


def generate_spoken_brief(search_results, config=None):
    config = config or {}
    with client.BedrockClient(api_key=config.get("api_key") or os.environ["AMAZON_BEDROCK_API_KEY"]) as client:
        response = client.models.generate_speech(text=search_results)
    return response.audio_url