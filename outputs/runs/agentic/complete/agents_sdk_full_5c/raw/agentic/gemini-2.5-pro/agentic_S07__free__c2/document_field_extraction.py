
import os
import json
from typing import Dict, Any
import anthropic

def extract_structured_fields(text: str, desired_schema: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extracts structured fields from text based on a JSON schema using Anthropic's Claude.

    Requires the ANTHROPIC_API_KEY environment variable to be set.

    Args:
        text: The unstructured text from a document.
        desired_schema: A dictionary representing the desired JSON schema.

    Returns:
        A dictionary with the extracted data.
    """
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable not set.")

    client = anthropic.Anthropic(api_key=api_key)

    prompt = f"""
    Given the following text, extract the information in a valid JSON object that conforms to the specified schema.
    
    Text:
    ---
    {text}
    ---
    
    JSON Schema:
    ---
    {json.dumps(desired_schema, indent=2)}
    ---
    
    Only output the JSON object. Do not include any other explanatory text.
    """

    message = client.messages.create(
        model="claude-3-sonnet-20240229",
        max_tokens=1024,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    response_text = message.content[0].text
    
    try:
        # Claude might wrap the JSON in ```json ... ```, so we find the object
        json_start = response_text.find('{')
        json_end = response_text.rfind('}') + 1
        if json_start != -1 and json_end != -1:
            json_string = response_text[json_start:json_end]
            return json.loads(json_string)
        else:
            raise json.JSONDecodeError("No JSON object found in response.", response_text, 0)
    except json.JSONDecodeError as e:
        # Handle cases where the output is not valid JSON
        print(f"Error decoding JSON from model response: {e}")
        return {"error": "Failed to extract valid JSON", "response": response_text}
