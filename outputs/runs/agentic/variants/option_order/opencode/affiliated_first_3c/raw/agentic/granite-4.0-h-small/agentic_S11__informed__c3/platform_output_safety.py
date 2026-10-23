# platform_output_safety.py
# [LATER-STEP] Check platform model output for unsafe content using watsonx guardrails

# Provider: IBM watsonx.ai (guardrails integration)
import json
from ibm_watsonx_ai import Client
from ibm_watsonx_ai.consts import ServiceType

WATSONX_API_KEY = os.getenv("WATSONX_API_KEY")
WATSONX_PROJECT_ID = os.getenv("WATSONX_PROJECT_ID")

# Load watsonx.ai credentials once
client = Client(
    url="https://api.ibm.com/watsonx",
    api_key=WATSONX_API_KEY,
    service_type=ServiceType.WATSONX_AI,
)


def is_safe(output: str, deployment_id: str) -> bool:
    """Check output with watsonx guardrails.
    Returns True if safe, False if flagged as unsafe.
    """
    # watsonx guardrails endpoint (hypothetical method name)
    # The SDK may expose `client.guardrails.check` in future; using REST payload here.
    resp = client.compliance_guardrails.check(
        deployment_id=deployment_id, content=output, content_type="text/plain"
    )
    # Result example: {"result": "PASS", "details": {...}}
    return resp.get("result") == "PASS"


if __name__ == "__main__":
    DEPLOY_ID = "my-wx-deployment"
    OUTPUT = "This is a harmless sentence."
    print(f"Safety check result: {is_safe(OUTPUT, DEPLOY_ID)}")
