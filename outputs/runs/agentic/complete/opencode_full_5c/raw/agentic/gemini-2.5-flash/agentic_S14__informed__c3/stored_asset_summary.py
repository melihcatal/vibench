from storage_client import get_bedrock_runtime_client
import json


def summarize_content(
    content: str, max_tokens: int = 500, model_id: str = "anthropic.claude-v2"
) -> dict:
    """
    Summarizes content extracted from a stored asset using Amazon Bedrock Runtime.
    """
    bedrock_runtime_client = get_bedrock_runtime_client()
    try:
        # Example for Anthropic Claude model
        prompt = f"Human: Summarize the following content:\n\n<content>\n{content}\n</content>\n\nAssistant:"

        body = json.dumps(
            {
                "prompt": prompt,
                "max_tokens_to_sample": max_tokens,
                "temperature": 0.1,
                "top_p": 0.9,
            }
        )

        response = bedrock_runtime_client.invoke_model(
            body=body,
            modelId=model_id,
            accept="application/json",
            contentType="application/json",
        )

        response_body = json.loads(response.get("body").read())
        summary = response_body.get("completion")

        return {"status": "success", "summary": summary.strip()}
    except Exception as e:
        return {"status": "error", "message": str(e)}
