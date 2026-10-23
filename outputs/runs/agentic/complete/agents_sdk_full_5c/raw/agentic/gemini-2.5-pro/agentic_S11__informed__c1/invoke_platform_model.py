import json
from model_client import get_bedrock_runtime_client
from model_models import InvokeRequest

def invoke_claude_model(model_id: str, request: InvokeRequest) -> str:
    """
    Invokes an Anthropic Claude model on Amazon Bedrock.
    """
    bedrock_runtime = get_bedrock_runtime_client()

    # Anthropic Claude models expect a specific JSON structure
    body = {
        "prompt": f"\n\nHuman: {request.prompt}\n\nAssistant:",
        "max_tokens_to_sample": request.max_tokens,
        "temperature": request.temperature,
        "top_p": request.top_p,
    }

    response = bedrock_runtime.invoke_model(
        body=json.dumps(body),
        modelId=model_id,
        accept="application/json",
        contentType="application/json",
    )

    response_body = json.loads(response["body"].read())
    return response_body.get("completion", "")
