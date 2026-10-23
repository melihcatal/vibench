import boto3
import os


def stream_completion(prompt: str) -> None:
    client = boto3.client(
        "bedrock-runtime",
        region_name="us-east-1",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    )

    content_type = "application/json"
    accept = "text/stream+json"

    payload = {
        "inputs": [
            {
                "inputText": prompt,
                "contentType": content_type,
            }
        ],
        "parameters": {
            "maxTokens": 512,
            "temperature": 0.7,
        },
    }
    request = {
        "ContentType": content_type,
        "Accept": accept,
        "Body": payload,
    }

    # Send streaming request to Bedrock
    response = client.invoke_model(
        ModelId="amazon.titan-text-express-v1.0",
        # Using streaming_endpoint_url is possible, but invoke_model supports streaming natively
        Body=request,
        # The returned iterator yields chunks of model output
    )

    # Print each chunk as it arrives (could be piped to a file or further processing)
    for chunk in response["Body"].iter_lines():
        print(chunk.decode())
