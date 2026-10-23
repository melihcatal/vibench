# validate_document_fields.py
import json
from typing import Dict, Any, List
from document_client import get_bedrock_client

def validate_document_fields_with_bedrock(
    extracted_fields: Dict[str, Any],
    confidence_scores: Dict[str, float]
) -> List[str]:
    """
    Validates extracted fields and their confidence scores using Amazon Bedrock.
    """
    client = get_bedrock_client()
    model_id = "anthropic.claude-3-sonnet-20240229-v1:0"

    prompt = f"""
        You are a validation engine for structured document extraction.
        Your task is to identify any validation errors in the provided data based on a set of rules.

        Rules:
        1. The following fields must be present: 'vendor_name', 'invoice_date', 'total_amount'.
        2. The 'total_amount' must be a positive number.
        3. All provided confidence scores must be greater than 0.85.

        Extracted Data:
        {json.dumps(extracted_fields, indent=2)}

        Confidence Scores:
        {json.dumps(confidence_scores, indent=2)}

        Analyze the data against the rules and return a JSON array of strings, where each string is a
        description of a validation error. If there are no errors, return an empty array.
        Respond ONLY with the JSON array.
    """

    payload = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 1024,
        "messages": [
            {
                "role": "user",
                "content": [{"type": "text", "text": prompt}],
            }
        ],
    }

    response = client.invoke_model(
        body=json.dumps(payload),
        modelId=model_id,
        contentType="application/json",
        accept="application/json",
    )

    response_body = json.loads(response.get("body").read())
    error_list_str = response_body["content"][0]["text"]
    
    try:
        errors = json.loads(error_list_str)
        if isinstance(errors, list):
            return errors
        else:
            return ["Validation model returned an unexpected format."]
    except json.JSONDecodeError:
        return [f"Failed to decode validation model response: {error_list_str}"]
