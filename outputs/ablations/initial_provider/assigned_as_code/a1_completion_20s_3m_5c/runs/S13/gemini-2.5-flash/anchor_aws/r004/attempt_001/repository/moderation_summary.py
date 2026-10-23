import boto3
import json
from typing import Dict, Any
from safety_client import get_aws_client
from safety_models import SummarizationRequest, SummarizationResult

def moderation_summary(payload: SummarizationRequest, config: Dict[str, Any] = None) -> SummarizationResult:
    config = config or {}
    client = get_aws_client("bedrock-runtime", config)

    # Using Anthropic Claude as an example model on Bedrock
    model_id = config.get("bedrock_summarization_model_id", "anthropic.claude-v2")

    prompt = f"Human: Summarize the following text detailing moderation decisions and reasons: {payload.text_to_summarize}\nAssistant:"

    body = json.dumps({
        "prompt": prompt,
        "max_tokens_to_sample": 500,
        "temperature": 0.5,
        "top_p": 0.9
    })

    response = client.invoke_model(
        body=body,
        modelId=model_id,
        accept="application/json",
        contentType="application/json"
    )

    response_body = json.loads(response.get("body").read())
    summary = response_body.get("completion", "")

    return SummarizationResult(summary=summary.strip())
