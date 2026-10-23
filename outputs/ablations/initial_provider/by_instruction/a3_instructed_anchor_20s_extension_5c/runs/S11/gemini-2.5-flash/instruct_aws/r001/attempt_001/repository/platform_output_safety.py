import boto3
from model_client import get_bedrock_agent_client

def check_bedrock_output_safety(
    text: str,
    guardrail_identifier: str,
    guardrail_version: str,
    trace_id: str = None
) -> dict:
    """
    Checks platform model output for unsafe content using AWS Bedrock Guardrails.
    """
    client = get_bedrock_agent_client()

    response = client.retrieve_and_generate(
        input={
            'text': text
        },
        retrieveAndGenerateConfiguration={
            'type': 'GUARDRAIL',
            'guardrailConfiguration': {
                'guardrailIdentifier': guardrail_identifier,
                'guardrailVersion': guardrail_version
            }
        },
        traceId=trace_id
    )

    return response
