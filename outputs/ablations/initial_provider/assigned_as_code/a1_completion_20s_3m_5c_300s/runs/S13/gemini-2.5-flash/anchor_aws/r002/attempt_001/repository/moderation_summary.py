import boto3
import json
from typing import Dict, Any
from safety_client import get_aws_client

def moderation_summary(payload: Dict[str, Any], config: Dict[str, Any] = None) -> Dict[str, Any]:
    config = config or {}
    client = get_aws_client("bedrock-runtime", region_name=config.get("region", "us-east-1"))
    
    text_to_summarize = payload["text"]
    
    # Using Anthropic Claude for summarization via Bedrock
    model_id = "anthropic.claude-v2"
    
    body = json.dumps({
        "prompt": f"\n\nHuman: Summarize the following text in a concise manner: {text_to_summarize}\n\nAssistant:",
        "max_tokens_to_sample": 200,
        "temperature": 0.1,
        "top_p": 0.9
    })
    
    response = client.invoke_model(
        body=body,
        modelId=model_id,
        accept="application/json",
        contentType="application/json"
    )
    
    response_body = json.loads(response.get("body").read())
    summary = response_body.get("completion")
    
    return {"summary": summary.strip()}
