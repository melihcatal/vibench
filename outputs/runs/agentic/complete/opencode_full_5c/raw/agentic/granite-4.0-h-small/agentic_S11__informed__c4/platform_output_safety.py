# platform_output_safety.py
# [LATER-STEP] Check platform model output for unsafe content

# Service: IBM watsonx.ai guardrails (example provider)
import os
from ibm_watsonx_ai import Client
from ibm_watsonx_ai.risk.services.content_safety import ContentSafety, ContentSafetyV2

WATSONX_API_KEY = os.getenv("WATSONX_API_KEY")
WATSONX_PROJECT_ID = os.getenv("WATSONX_PROJECT_ID")

# Instantiate the guardrails client (SDK)
guardrails = ContentSafetyV2(
    service_endpoint="https://api.watsonx.ibm.com",
    api_key=WATSONX_API_KEY,
    project_id=WATSONX_PROJECT_ID,
)


def is_safe(output_text: str) -> bool:
    """Return True if the output passes watsonx.ai guardrails, False otherwise."""
    result = guardrails.analyze_content(content=output_text)
    # IBM guardrails return a boolean `is_safe` field
    return result.get("is_safe", False)


# Example local usage (no real API call expected in this sandbox)
if __name__ == "__main__":
    test_output = "This is a safe statement."
    print("Safe?", is_safe(test_output))
