# validate_document_fields.py
import json
from typing import Dict, Any
from document_client import get_anthropic_client

def validate_fields_with_confidence(
    raw_fields: Dict[str, Any],
    required_fields: list[str],
    min_confidence: float,
) -> Dict[str, Any]:
    """
    Validates extracted fields and confidence scores using Anthropic's Claude.
    """
    client = get_anthropic_client()
    
    prompt = f"""
    You are a validation expert for a document processing system.
    Your task is to analyze the following extracted fields and their confidence scores.

    Validation Rules:
    1. Check if all required fields are present in the 'raw_fields' object.
    2. For each required field, check if its confidence score is at or above the minimum threshold.
    3. List any missing required fields.
    4. List any fields that are present but have a confidence score below the threshold.

    Data:
    - Required Fields: {required_fields}
    - Minimum Confidence Threshold: {min_confidence}
    - Extracted Raw Fields (with values and confidence scores):
    {json.dumps(raw_fields, indent=2)}

    Please provide a response in the following JSON format:
    {{
      "validation_passed": boolean,
      "missing_fields": ["field1", "field2", ...],
      "low_confidence_fields": [{{ "field": "field_name", "confidence": 0.xx }}]
    }}
    """
    
    message = client.messages.create(
        model="claude-3-sonnet-20240229",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )
    
    response_text = message.content[0].text
    
    # Clean the response to extract only the JSON object
    json_str = response_text[response_text.find('{'):response_text.rfind('}')+1]
    
    try:
        validation_result = json.loads(json_str)
        return validation_result
    except json.JSONDecodeError:
        raise ValueError("Failed to parse validation result from Anthropic response.")
