import json
from typing import Dict, Any

from speech_client import get_bedrock_runtime_client

def archive_summary(text: str, config: Dict[str, Any] = None) -> str:
    config = config or {}
    client = get_bedrock_runtime_client(region_name=config.get("region"))
    
    # Using Anthropic Claude as an example model for summarization
    # Model ID can be configured or passed in payload
    model_id = config.get("bedrock_summary_model_id", "anthropic.claude-v2")
    
    body = json.dumps({
        "prompt": f"\n\nHuman: Summarize the following text:\n\n<text>\n{text}\n</text>\n\nAssistant:",
        "max_tokens_to_sample": 200,
        "temperature": 0.5,
    })
    
    response = client.invoke_model(
        body=body,
        modelId=model_id,
        accept="application/json",
        contentType="application/json"
    )
    
    response_body = json.loads(response.get("body").read())
    return response_body.get("completion", "")
