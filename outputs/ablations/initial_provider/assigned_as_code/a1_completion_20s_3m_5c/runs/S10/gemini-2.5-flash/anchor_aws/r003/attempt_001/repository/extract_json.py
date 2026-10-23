import boto3
from model_client import BedrockClient
from model_models import ConverseRequest, Message

def extract_json(payload, config=None):
    config = config or {}
    bedrock_client = BedrockClient(region_name=config.get("region", "us-east-1"))
    prompt_text = (
        "Extract the following information as a JSON object from the text below:\n\n"
        + payload["text"]
        + "\n\nReturn only the JSON object, do not include any other text."
    )

    request = ConverseRequest(
        model_id="amazon.nova-pro-v1:0",
        messages=[
            Message(role="user", content=[{"text": prompt_text}])
        ],
        max_tokens=2048, # Increased token limit for potentially larger JSON outputs
        temperature=0.0, # Lower temperature for structured output
    )

    response = bedrock_client.converse(request)
    return {"json_output": response.text}
