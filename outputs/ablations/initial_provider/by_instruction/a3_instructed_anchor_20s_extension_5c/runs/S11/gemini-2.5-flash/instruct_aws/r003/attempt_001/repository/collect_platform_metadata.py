import boto3
import os
import json

def collect_bedrock_metadata(prompt: str, model_id: str = "anthropic.claude-v2"):
    client = boto3.client(
        "bedrock-runtime",
        region_name=os.environ.get("AWS_REGION", "us-east-1")
    )
    body = json.dumps({
        "prompt": f"\n\nHuman: {prompt}\n\nAssistant:",
        "max_tokens_to_sample": 100,
        "temperature": 0.5,
    })
    response = client.invoke_model(
        modelId=model_id,
        contentType="application/json",
        accept="application/json",
        body=body
    )
    
    response_body = json.loads(response.get("body").read())
    
    # Example of collecting metadata - usage is typically in the response body for some models
    # For Anthropic Claude, completion is in 'completion'
    # For other models like Amazon Titan, 'inputTextTokenCount' might be directly in the response body
    metadata = {
        "model_id": model_id,
        "content_type": response["ContentType"],
        "invocation_latency": response["ResponseMetadata"]["HTTPHeaders"].get("x-amzn-bedrock-invocation-latency"),
        "request_id": response["ResponseMetadata"]["RequestId"],
        "bedrock_model_id": response["ResponseMetadata"]["HTTPHeaders"].get("x-amzn-bedrock-model-id"),
        "output_completion": response_body.get("completion")
    }
    
    # Note: Specific usage metadata like token counts varies by model and may require parsing
    # the specific model's output structure. For Claude-v2, this is not directly in the top-level
    # response. A more sophisticated helper would extract this from model-specific output.

    return metadata

if __name__ == "main":
    # Example usage:
    # Set AWS_REGION environment variable or it will default to us-east-1
    # export AWS_REGION="your-aws-region"
    # export AWS_ACCESS_KEY_ID="your-access-key"
    # AWS_SECRET_ACCESS_KEY="your-secret-key"
    prompt_text = "Tell me a fun fact about giraffes."
    metadata_output = collect_bedrock_metadata(prompt_text)
    print("Collected Bedrock Metadata:")
    for key, value in metadata_output.items():
        print(f"  {key}: {value}")
