import os
from amazon.bedrock import client


def translate_query(query, target_language, config=None):
    config = config or {}
    with client.BedrockClient(api_key=config.get("api_key") or os.environ["AMAZON_BEDROCK_API_KEY"]) as client:
        response = client.models.translate_text(text=query, target_language=target_language)
    return response.translated_text