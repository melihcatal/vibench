import json
from storage_client import get_bedrock_runtime_client
from storage_models import SummaryRequest


def summarize_asset_content(request: SummaryRequest) -> str:
    """
    Summarizes text content using Amazon Bedrock with Anthropic Claude.
    """
    bedrock_client = get_bedrock_runtime_client()

    prompt = f"\n\nHuman: Please provide a concise summary of the following text:\n\n{request.text}\n\nAssistant:"

    body = json.dumps(
        {
            "prompt": prompt,
            "max_tokens_to_sample": 300,
            "temperature": 0.1,
            "top_p": 0.9,
        }
    )

    model_id = "anthropic.claude-v2"
    response = bedrock_client.invoke_model(
        body=body,
        modelId=model_id,
        accept="application/json",
        contentType="application/json",
    )

    response_body = json.loads(response.get("body").read())

    return response_body.get("completion")
