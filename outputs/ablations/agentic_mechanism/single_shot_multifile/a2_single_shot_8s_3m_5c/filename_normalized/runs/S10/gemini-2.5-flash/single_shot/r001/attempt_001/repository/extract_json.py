import json
from typing import Dict, Any
from model_client import get_anthropic_client

def extract_json(text: str, schema: Dict[str, Any]) -> Dict[str, Any]:
    client = get_anthropic_client()
    model_id = "claude-3-opus-20240229"
    prompt_template = """
    Extract information from the provided text into a JSON object that strictly conforms to the following JSON schema.
    Do not include any other text or explanation, only the JSON object.

    JSON Schema:
    {}

    Text to extract from:
    {}

    Extracted JSON:
    """.format(json.dumps(schema, indent=2), text)

    response = client.messages.create(
        model=model_id,
        max_tokens=2000,
        messages=[
            {"role": "user", "content": prompt_template}
        ],
        temperature=0.0,
    )
    json_str = response.content[0].text
    try:
        return json.loads(json_str)
    except json.JSONDecodeError:
        return {}