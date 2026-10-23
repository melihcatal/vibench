from model_client import BedrockModelClient
from model_models import JsonPayload
import json

def extract_json(payload: JsonPayload, config=None):
    client = BedrockModelClient(region_name=config.get("region") if config else None)
    
    prompt = f"""Extract JSON from the following text based on the provided JSON schema. Only return the JSON object.

Text: {payload.text}

JSON Schema: {json.dumps(payload.json_schema, indent=2)}

Extracted JSON:"""

    messages = [
        {"role": "user", "content": [{"text": prompt}]}
    ]

    # Use a stronger model for JSON extraction if available, otherwise default
    # For this example, we'll stick to the default configured in model_client.py or explicitly set
    response = client.invoke_llm(
        messages=messages,
        inference_config={
            "maxTokens": 2048,
            "temperature": 0.1, # Low temperature for structured output
            "topP": 0.9
        },
        model_id="anthropic.claude-3-haiku-20240307-v1:0" # Using Claude 3 Haiku for better JSON capabilities
    )
    
    extracted_text = "".join(block.text for block in response.output.message.content if block.text)
    try:
        return {"json_output": json.loads(extracted_text)}
    except json.JSONDecodeError:
        return {"json_output": {}, "error": "Failed to decode JSON", "raw_output": extracted_text}
