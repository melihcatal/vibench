import boto3
from model_client import BedrockClient
from model_models import ConverseRequest, Message

def stream_completion(payload, config=None):
    config = config or {}
    bedrock_client = BedrockClient(region_name=config.get("region", "us-east-1"))
    
    prompt_text = payload.get("prompt", "")

    request = ConverseRequest(
        model_id="amazon.nova-pro-v1:0",
        messages=[
            Message(role="user", content=[{"text": prompt_text}])
        ],
        max_tokens=1024,
        temperature=0.7,
    )

    stream_iterator = bedrock_client.converse_stream(request)
    
    for chunk in stream_iterator:
        if "text" in chunk:
            yield {"token": chunk["text"]}
        elif "stop_reason" in chunk:
            yield {"stop_reason": chunk["stop_reason"]}
        elif "input_tokens" in chunk:
            yield {"input_tokens": chunk["input_tokens"], "output_tokens": chunk["output_tokens"]}
