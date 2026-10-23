import boto3
import json
import os

def extract_json(text: str, schema: dict, model_id: str = "anthropic.claude-3-sonnet-20240229-v1:0") -> dict:
    """
    Extracts structured JSON from text using an AWS Bedrock LLM.
    """
    client = boto3.client(
        service_name="bedrock-runtime",
        region_name=os.environ.get("AWS_REGION", "us-east-1"),
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
    )

    schema_str = json.dumps(schema, indent=2)

    prompt = f"""Human: You are an AI assistant that extracts information from text into a JSON format.
Given the following text, extract information that matches the provided JSON schema.

Text:
{text}

JSON Schema:
{schema_str}

Assistant: Here is the extracted JSON:
"""

    body = json.dumps({
        "prompt": prompt,
        "max_tokens_to_sample": 2000,
        "temperature": 0.1,
    })

    response = client.invoke_model(
        body=body,
        modelId=model_id,
        accept="application/json",
        contentType="application/json"
    )

    response_body = json.loads(response.get("body").read())
    completion = response_body.get("completion")

    # Attempt to parse the completion as JSON
    try:
        # Claude often returns the JSON embedded in text, sometimes with ```json``` fences.
        # Try to find the first and last curly braces to extract pure JSON.
        start_brace = completion.find('{')
        end_brace = completion.rfind('}')
        if start_brace != -1 and end_brace != -1 and end_brace > start_brace:
            json_str = completion[start_brace : end_brace + 1]
            return json.loads(json_str)
        else:
            # If no braces, try direct parsing (less likely to succeed if not pure JSON)
            return json.loads(completion)
    except json.JSONDecodeError:
        print(f"Warning: Could not decode JSON from LLM response: {completion}")
        return {}
