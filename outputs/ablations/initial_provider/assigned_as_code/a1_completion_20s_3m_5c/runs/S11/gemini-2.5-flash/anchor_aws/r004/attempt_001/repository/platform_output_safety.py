import boto3

def check_platform_output_safety(text: str, config=None):
    config = config or {}
    region = config.get("region", "us-east-1")
    
    # Using Bedrock Guardrails for content moderation
    # Note: Guardrails need to be created and configured in AWS Bedrock beforehand.
    # This example assumes a guardrail is already set up.
    
    client = boto3.client("bedrock-runtime", region_name=region)
    
    # Replace with your actual Guardrail ID and Guardrail Version
    guardrail_id = config.get("guardrail_id", "GUARDRAIL_ID_PLACEHOLDER")
    guardrail_version = config.get("guardrail_version", "DRAFT")

    if guardrail_id == "GUARDRAIL_ID_PLACEHOLDER":
        print("Warning: Please configure a valid Guardrail ID for safety checks.")
        return {"safe": True, "violations": []}

    response = client.apply_guardrail(
        guardrailIdentifier=guardrail_id,
        guardrailVersion=guardrail_version,
        content=[{
            'text': {
                'text': text,
                'qualifier': 'base'
            }
        }],
        source='INPUT', # Can be INPUT or OUTPUT depending on where the text comes from
    )

    violations = []
    if response.get('usage', {}).get('topicPolicy', {}).get('violations'):
        for violation in response['usage']['topicPolicy']['violations']:
            violations.append({"type": "TOPIC_POLICY", "risk": violation['risk'], "text": violation['violations']})

    # You might also check other policies like content policy, word policy etc.

    is_safe = not bool(violations)

    return {"safe": is_safe, "violations": violations, "guardrail_response": response}
