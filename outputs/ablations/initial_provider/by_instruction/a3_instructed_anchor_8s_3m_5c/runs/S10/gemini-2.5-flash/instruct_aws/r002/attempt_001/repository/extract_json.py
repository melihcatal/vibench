import boto3
import json

def extract_json(text: str, schema: dict) -> dict:
    """
    Calls AWS Bedrock to extract structured JSON from the given text based on a schema.
    """
    bedrock_runtime = boto3.client(
        service_name="bedrock-runtime",
        region_name="us-east-1"
    )

    prompt = f"""Human: Extract information from the following text into a JSON object that conforms to the provided JSON schema.
Text: <text>{text}</text>
Schema: <schema>{json.dumps(schema)}</schema>
Assistant:"""

    body = json.dumps({
        "prompt": prompt,
        "max_tokens_to_sample": 1000,
        "temperature": 0.1,
        "top_p": 0.9
    })

    model_id = "anthropic.claude-v2"
    content_type = "application/json"
    accept = "application/json"

    response = bedrock_runtime.invoke_model(
        body=body,
        modelId=model_id,
        contentType=content_type,
        accept=accept
    )

    response_body = json.loads(response.get("body").read())
    completion = response_body.get("completion").strip()
    try:
        return json.loads(completion)
    except json.JSONDecodeError:
        # Handle cases where the model might not return perfect JSON
        print(f"Warning: Model did not return perfect JSON: {completion}")
        return {}

