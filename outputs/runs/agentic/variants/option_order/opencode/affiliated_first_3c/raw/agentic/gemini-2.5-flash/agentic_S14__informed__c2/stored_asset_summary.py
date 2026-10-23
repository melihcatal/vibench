import json
from storage_client import get_bedrock_runtime_client


def summarize_stored_asset_content(content: str) -> str:
    """
    Summarizes content extracted from a stored asset using an Amazon Bedrock LLM (Titan model).
    """
    bedrock_runtime_client = get_bedrock_runtime_client()

    prompt = f"Human: Summarize the following text:\n\n{content}\n\nAssistant:"

    body = json.dumps(
        {
            "prompt": prompt,
            "max_tokens_to_sample": 500,  # Max length of the generated response
            "temperature": 0.7,  # Controls randomness
            "top_p": 0.9,  # Nucleus sampling
        }
    )

    response = bedrock_runtime_client.invoke_model(
        body=body,
        modelId="anthropic.claude-v2",  # Using Claude V2 as an example. Other models like Amazon Titan Text G1 - Express can also be used.
        accept="application/json",
        contentType="application/json",
    )

    response_body = json.loads(response.get("body").read())
    return response_body.get("completion")
