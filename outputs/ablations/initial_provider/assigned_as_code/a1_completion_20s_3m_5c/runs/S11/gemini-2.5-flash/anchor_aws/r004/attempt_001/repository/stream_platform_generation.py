import boto3

def stream_platform_generation(payload, config=None):
    config = config or {}
    client = boto3.client("bedrock-runtime", region_name=config.get("region", "us-east-1"))
    
    # Using invoke_model_with_response_stream for streaming capabilities
    # This requires a different model invocation payload structure than 'converse'
    # For simplicity, we'll adapt the payload to a common text generation model like Anthropic Claude.
    
    # Example with Anthropic Claude on Bedrock
    model_id = config.get("model_id", "anthropic.claude-3-sonnet-20240229-v1:0") # Using Claude 3 Sonnet for streaming
    
    body = {
        "anthropic_version": "bedrock-2023-05-31",
        "messages": [
            {
                "role": "user",
                "content": payload["text"],
            }
        ],
        "max_tokens": 100,
        "temperature": 0.5,
    }

    response = client.invoke_model_with_response_stream(
        modelId=model_id,
        contentType="application/json",
        accept="application/json",
        body=body
    )

    for event in response['body']:
        chunk = event.get('chunk')
        if chunk:
            # Decode the bytes and then parse the JSON string
            parsed_chunk = chunk['bytes'].decode('utf-8')
            # In a real scenario, you'd parse 'parsed_chunk' as JSON
            # For this example, we'll just yield the raw chunk bytes to demonstrate streaming
            yield {"raw_chunk_bytes": parsed_chunk}
