from model_client import bedrock_runtime, load_model_config, stream_model


def stream_completion(prompt: str):
    config = load_model_config("anthropic.claude-3-haiku-20240307-v1:0")
    client = bedrock_runtime(config.region)
    payload = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 256,
        "temperature": 0.2,
        "messages": [{"role": "user", "content": prompt}],
    }
    for chunk in stream_model(client, config.model_id, payload):
        yield chunk
