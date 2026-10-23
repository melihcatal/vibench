import boto3
import json

def summarize_text(text: str) -> str:
    """
    Calls AWS Bedrock to summarize the given text using an LLM.
    """
    bedrock_runtime = boto3.client(
        service_name="bedrock-runtime",
        region_name="us-east-1"
    )
    
    prompt = f"""Human: Summarize the following text:
<text>
{text}
</text>
Assistant:"""

    body = json.dumps({
        "prompt": prompt,
        "max_tokens_to_sample": 300,
        "temperature": 0.5,
        "top_p": 0.9
    })
    
    model_id = "anthropic.claude-v2"
    content_type = "application/json"
    accept = "application/json"

    response = bedrock_runtime.invoke_model(
        body=body,
        modelId=model_id,
        contentType=content_type,
        accept=accept
    )
    
    response_body = json.loads(response.get("body").read())
    return response_body.get("completion")

