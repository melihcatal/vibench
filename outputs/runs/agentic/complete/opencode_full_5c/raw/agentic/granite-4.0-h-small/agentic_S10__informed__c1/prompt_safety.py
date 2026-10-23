# Later-step: unsafe content moderation
import os
from model_client import get_text_chat_client

# Example using WatsonX guardrails / Amazon Bedrock Guardrails
# The moderation function works with any provider – config via env vars


def is_safe(prompt: str, model: str = "granite-4") -> bool:
    """Check whether text is safe for downstream processing.

    Args:
        prompt: The raw user or model-generated text to evaluate.
        model: Provider identifier (default: "granite-4").

    Returns:
        True if the content passes moderation, False otherwise.
    """
    client = get_text_chat_client(model)

    # ---- WatsonX Guardrails (requires WATSONX_API_KEY, WATSONX_PROJECT_ID) ----
    if model == "granite-4":
        # Use HAP detection endpoint (simplified call)
        resp = client.check_compliance(prompt, compliance_category="public")
        return resp.get("compliant", False)

    # ---- Amazon Bedrock Guardrails ----
    if model == "bedrock":
        # Bedrock Guardrails API (requires AWS credentials)
        from boto3 import client as boto3_client

        bedrock = boto3_client("bedrock-runtime")
        request_body = {"content": prompt, "contentType": "text/plain"}
        # Guardrails check – assumes Guardrails endpoint is exposed via runtime
        # Here we simulate with a dummy call; real implementation will differ
        guard_resp = bedrock.invoke_endpoint(
            EndpointName=os.getenv("BEDROCK_GUARD_ENDPOINT"),
            ContentType="text/plain",
            Body=prompt.encode("utf-8"),
        )
        result = guard_resp["Body"].read().decode()
        return result.strip().lower() == "safe"

    # ---- Default: use Perspective API (REST) ----
    # Requires PERSPECTIVE_API_KEY env var
    import requests

    resp = requests.post(
        "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze",
        json={"comment": {"text": prompt}, "requestedAttributes": {"TOXICITY": {}}},
        headers={"apiKey": os.getenv("PERSPECTIVE_API_KEY")},
    )
    return resp.json()["attributeScores"]["TOXICITY"]["summaryScore"]["value"] < 0.5


# Simple usage example
# print(is_safe("Hey, let's talk about..."))
