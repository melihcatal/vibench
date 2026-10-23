import boto3
import os
import json

def stream_bedrock_generation(prompt: str, model_id: str = "anthropic.claude-v2"):
    client = boto3.client(
        "bedrock-runtime",
        region_name=os.environ.get("AWS_REGION", "us-east-1")
    )
    body = json.dumps({
        "prompt": f"\n\nHuman: {prompt}\n\nAssistant:",
        "max_tokens_to_sample": 500,
        "temperature": 0.5,
        "stop_sequences": ["\n\nHuman:"]
    })
    response = client.invoke_model_with_response_stream(
        modelId=model_id,
        contentType="application/json",
        accept="application/json",
        body=body
    )

    stream = response.get("body")
    if stream:
        for event in stream:
            chunk = event.get("chunk")
            if chunk:
                yield json.loads(chunk.get("bytes").decode()).get("completion")

if __name__ == "__main__":
    # Example usage:
    # Set AWS_REGION environment variable or it will default to us-east-1
    # export AWS_REGION="your-aws-region"
    # export AWS_ACCESS_KEY_ID="your-access-key"
    # export AWS_SECRET_ACCESS_KEY="your-secret-key"
    prompt_text = "Write a short story about a robot who discovers a love for painting."
    print("Streaming response:")
    full_response = ""
    for part in stream_bedrock_generation(prompt_text):
        print(part, end='')
        full_response += part
    print(f"\n\nFull response collected: {full_response}")
