from typing import Optional

from storage_client import get_bedrock_runtime_client


def stored_asset_summary(text: str, region: Optional[str] = None, model_id: str = "anthropic.claude-3-haiku-20240307-v1:0") -> str:
    bedrock = get_bedrock_runtime_client(region)
    payload = {"messages": [{"role": "user", "content": [{"type": "text", "text": f"Summarize the following content:\n{text}"}]}], "max_tokens": 200, "anthropic_version": "bedrock-2023-05-31"}
    response = bedrock.invoke_model(modelId=model_id, body=str(payload).replace("'", '"'))
    return response["body"].read().decode("utf-8")
