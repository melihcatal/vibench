import os
from model_client import get_bedrock_client
from model_models import BedrockConverseResponse
import json


def extract_json(payload, config=None):
    config = config or {}
    client = get_bedrock_client()
    
    prompt = (
        "Extract structured JSON from the following text. The JSON should conform to the following schema:\n"
        f"{json.dumps(payload['schema'], indent=2)}\n\n"
        "Text to extract from:\n"
        f"{payload['text']}\n\n"
        "JSON:"
    )

    response = client.converse(
        modelId=os.environ.get("BEDROCK_MODEL_ID", "anthropic.claude-3-sonnet-20240229-v1:0"),
        messages=[{"role": "user", "content": [{"text": prompt}]}],
        inferenceConfig={
            "maxTokens": config.get("max_tokens", 2000),
            "temperature": config.get("temperature", 0.1),
        },
    )
    
    text_content = "".join(block["text"] for block in response["output"]["message"]["content"] if "text" in block)
    
    try:
        return json.loads(text_content)
    except json.JSONDecodeError:
        # Fallback for when Bedrock might return non-json or partial json.
        # In a real scenario, you might want to log this or refine the prompt.
        return {"error": "Failed to parse JSON", "raw_output": text_content}
