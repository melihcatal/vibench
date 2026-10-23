import boto3
import os
import json

def extract_json(text: str, schema: dict) -> dict:
    client = boto3.client(
        service_name="bedrock-runtime",
        region_name=os.environ.get("AWS_REGION", "us-east-1"),
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
    )
    
    model_id = "anthropic.claude-3-sonnet-20240229-v1:0"
    
    prompt = f"""
    Human: Extract information from the following text into a JSON object that conforms to the provided JSON schema. Only return the JSON object.

    Text:
    <text>
    {text}
    </text>

    JSON Schema:
    <schema>
    {json.dumps(schema, indent=2)}
    </schema>

    Assistant:
    """
    
    body = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 1000,
        "messages": [
            {
                "role": "user",
                "content": [{"type": "text", "text": prompt}]
            }
        ]
    }
    
    response = client.invoke_model(
        body=json.dumps(body),
        modelId=model_id,
        accept="application/json",
        contentType="application/json"
    )
    
    response_body = json.loads(response.get("body").read())
    json_output_str = response_body["content"][0]["text"]
    
    # Attempt to parse the JSON string. Claude sometimes wraps it in markdown.
    try:
        if json_output_str.startswith("```json") and json_output_str.endswith("```"):
            json_output_str = json_output_str[len("```json"):-len("```")].strip()
        return json.loads(json_output_str)
    except json.JSONDecodeError:
        print("Warning: LLM did not return valid JSON. Attempting fallback.")
        # Fallback if the LLM output isn't directly parsable
        return json.loads("{}") # Return an empty dict or handle error appropriately

if __name__ == '__main__':
    # Example usage:
    sample_text = "The user's name is John Doe, and he is 30 years old. His email is john.doe@example.com."
    sample_schema = {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "age": {"type": "integer"},
            "email": {"type": "string"}
        },
        "required": ["name", "age", "email"]
    }
    extracted_data = extract_json(sample_text, sample_schema)
    print("Extracted JSON:", json.dumps(extracted_data, indent=2))
