import boto3
import os
import json

def collect_bedrock_output_and_metadata(prompt: str, model_id: str = "anthropic.claude-v2"):
    """
    Invokes a Bedrock model and returns the output along with selected platform metadata.
    """
    client = boto3.client(
        "bedrock-runtime",
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        region_name=os.environ.get("AWS_REGION", "us-east-1")
    )
    
    body = {
        "prompt": f"Human: {prompt}\n\nAssistant:",
        "max_tokens_to_sample": 200,
        "temperature": 0.7,
        "top_p": 0.9
    }
    
    response = client.invoke_model(
        body=json.dumps(body),
        modelId=model_id,
        accept="application/json",
        contentType="application/json"
    )
    
    response_body = json.loads(response['body'].read().decode('utf-8'))
    
    output = response_body.get('completion')
    
    # Bedrock runtime does not return usage directly in invoke_model,
    # but the response header contains some info.
    # For more detailed metadata, one might need to parse logs or use higher-level SDK features.
    metadata = {
        "model_id_used": model_id,
        "response_content_type": response['ResponseMetadata']['HTTPHeaders']['content-type'],
        "request_id": response['ResponseMetadata']['RequestId']
    }
    
    return {"output": output, "metadata": metadata}
