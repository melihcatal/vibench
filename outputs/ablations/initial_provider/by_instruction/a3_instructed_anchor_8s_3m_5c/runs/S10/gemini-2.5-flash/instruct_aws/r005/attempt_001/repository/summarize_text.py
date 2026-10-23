import boto3
import json
import os

def summarize_text(text: str) -> str:
    """
    Calls AWS Bedrock to summarize the given text.
    """
    # AWS Bedrock client
    bedrock_runtime = boto3.client(
        service_name='bedrock-runtime',
        region_name=os.environ.get('AWS_REGION', 'us-east-1')
    )

    prompt = f"""Human: Summarize the following text:

    <text>
    {text}
    </text>

    Assistant:"""

    body = json.dumps({
        "prompt": prompt,
        "max_tokens_to_sample": 500,
        "temperature": 0.5,
        "top_p": 0.9
    })

    model_id = "anthropic.claude-v2" # Example model ID, replace if needed
    response = bedrock_runtime.invoke_model(
        modelId=model_id,
        contentType="application/json",
        accept="application/json",
        body=body
    )

    response_body = json.loads(response.get("body").read())
    return response_body.get("completion")
