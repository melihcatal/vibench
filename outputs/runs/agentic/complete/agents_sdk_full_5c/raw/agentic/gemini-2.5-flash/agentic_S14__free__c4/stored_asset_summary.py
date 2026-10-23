import json
from typing import Optional
from dataclasses import dataclass
from storage_client import get_bedrock_runtime_client

@dataclass
class StoredAssetSummaryRequest:
    text_content: str
    max_tokens: int = 500
    temperature: float = 0.5
    model_id: str = "anthropic.claude-v2"

@dataclass
class StoredAssetSummaryResponse:
    success: bool
    message: str
    summary_text: Optional[str] = None

def summarize_stored_asset_content(
    request: StoredAssetSummaryRequest
) -> StoredAssetSummaryResponse:
    """
    Summarizes content extracted from a stored asset using AWS Bedrock (Anthropic Claude).
    """
    bedrock_runtime = get_bedrock_runtime_client()

    try:
        prompt = f"Human: Summarize the following text:\n\n<text>\n{request.text_content}\n</text>\n\nAssistant:"

        body = json.dumps({
            "prompt": prompt,
            "max_tokens_to_sample": request.max_tokens,
            "temperature": request.temperature,
            "stop_sequences": ["\n\nHuman:"]
        })

        response = bedrock_runtime.invoke_model(
            body=body,
            modelId=request.model_id,
            accept="application/json",
            contentType="application/json"
        )

        response_body = json.loads(response.get("body").read())
        summary = response_body.get("completion")

        return StoredAssetSummaryResponse(
            success=True,
            message="Content summarized successfully",
            summary_text=summary.strip()
        )
    except Exception as e:
        return StoredAssetSummaryResponse(success=False, message=f"Error summarizing content with Bedrock: {str(e)}")
