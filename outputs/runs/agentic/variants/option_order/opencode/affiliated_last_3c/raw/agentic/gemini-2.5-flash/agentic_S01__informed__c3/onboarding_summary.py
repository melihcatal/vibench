import os
import sys
import json
import boto3

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from identity_client import IdentityClient
from identity_models import SummarizeRequest, SummarizeResponse


def onboarding_summary(request: SummarizeRequest) -> SummarizeResponse:
    identity_client = IdentityClient()
    bedrock_runtime = identity_client.get_bedrock_runtime_client()

    try:
        # Using Anthropic Claude on Bedrock for summarization
        model_id = "anthropic.claude-v2"
        # model_id = "anthropic.claude-3-sonnet-20240229-v1:0" # Example of a newer model

        body = json.dumps(
            {
                "prompt": f"\n\nHuman: Summarize the following onboarding state for support personnel, highlighting key information and any incomplete steps: {request.text}\n\nAssistant:",
                "max_tokens_to_sample": 500,
                "temperature": 0.5,
                "top_p": 0.9,
            }
        )

        response = bedrock_runtime.invoke_model(
            body=body,
            modelId=model_id,
            accept="application/json",
            contentType="application/json",
        )

        response_body = json.loads(response.get("body").read())
        summary = response_body.get("completion")

        return SummarizeResponse(summary=summary.strip())
    except Exception as e:
        return SummarizeResponse(summary=f"Summarization failed: {str(e)}")
