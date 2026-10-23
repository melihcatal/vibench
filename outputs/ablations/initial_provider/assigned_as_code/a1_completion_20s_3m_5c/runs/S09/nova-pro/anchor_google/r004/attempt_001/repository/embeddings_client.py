import os


def get_bedrock_client(api_key=None):
    api_key = api_key or os.environ.get('AMAZON_BEDROCK_API_KEY')
    if not api_key:
        raise ValueError('API key is required to create a Bedrock client')
    from amazon.bedrock import client
    return client.BedrockClient(api_key=api_key)


def normalize_payload(payload):
    normalized_payload = {}
    for key, value in payload.items():
        if isinstance(value, str):
            normalized_payload[key] = value.strip()
        elif isinstance(value, list):
            normalized_payload[key] = [item.strip() for item in value]
        else:
            normalized_payload[key] = value
    return normalized_payload