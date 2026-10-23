import os
import json
import boto3 # AWS SDK

def stream_bedrock_generation(model_id: str, prompt_content: str):
    client = boto3.client(
        'bedrock-runtime',
        region_name=os.environ.get("AWS_REGION", "us-east-1") # Provider-specific region
    ) # Provider-specific client

    body = json.dumps({
        "prompt": prompt_content,
        "max_tokens_to_sample": 300,
        "temperature": 0.5,
        "top_p": 0.9
    })

    response = client.invoke_model_with_response_stream(
        modelId=model_id, # Provider-specific model ID
        contentType="application/json",
        accept="application/json",
        body=body
    )

    event_stream = response.get('body')
    for event in event_stream:
        chunk = event.get('chunk')
        if chunk:
            chunk_obj = json.loads(chunk.get('bytes').decode())
            text = chunk_obj.get('completion')
            if text:
                yield text
    
    # Example of accessing provider response object, though stream events are chunks
    # Full response object is not available until stream ends, for streamed data.
    # We yield the text content to preserve the output while streaming.

if __name__ == '__main__':
    model_id = "ai21.j2-mid-v1" # Example Bedrock model ID (Jura-2 Mid)
    prompt = "Write a short poem about a serene mountain lake, streaming the output."

    print(f"Streaming from Amazon Bedrock model {model_id}...")
    full_output = []
    for text_chunk in stream_bedrock_generation(model_id, prompt):
        print(text_chunk, end='')
        full_output.append(text_chunk)
    print("\n\nStream complete. Full output length:", len("".join(full_output)))
