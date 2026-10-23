import os
import json
from security_client import get_bedrock_runtime_client


def summarize_rotation_status(audit_notes: str) -> str:
    """
    Summarizes secret rotation status using Amazon Bedrock Runtime with an LLM.
    """
    client = get_bedrock_runtime_client()
    model_id = "anthropic.claude-3-haiku-20240307-v1:0"  # Example model ID

    prompt = f"""Human: Summarize the following secret rotation audit notes:

<notes>
{audit_notes}
</notes>

Assistant:"""

    body = json.dumps(
        {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 200,
            "messages": [
                {"role": "user", "content": [{"type": "text", "text": prompt}]}
            ],
        }
    )

    try:
        response = client.invoke_model(
            body=body,
            modelId=model_id,
            accept="application/json",
            contentType="application/json",
        )
        response_body = json.loads(response.get("body").read())
        summary = response_body["content"][0]["text"]
        return summary
    except Exception as e:
        raise RuntimeError(f"Error summarizing rotation status with Bedrock: {e}")
