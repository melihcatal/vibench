import os
import json
from ibm_watsonx_ai import WatsonxApi

# Initialize Watsonx client using env vars (security_client may also provide this)
WATSONX_API_KEY = os.getenv("WATSONX_API_KEY")
WATSONX_PROJECT_ID = os.getenv("WATSONX_PROJECT_ID")
watsonx = WatsonxApi(base_url="https://api.watsonx.cloud", api_key=WATSONX_API_KEY)


def payload_safety(decrypted_text: str) -> bool:
    """Check decrypted text payload for unsafe content using Watsonx AI guardrails.

    Returns True if the content is safe, False if unsafe.
    """
    try:
        # Use Watsonx AI guardrails endpoint (simple request returning a boolean)
        response = watsonx.ai_projects.evaluate(
            project_id=WATSONX_PROJECT_ID,
            model_id="watsonx/moderation",
            text=decrypted_text,
        )
        # The response format is simplified; actual API may have a field like 'is_safe'
        result = response.json()
        safe = result.get("is_safe", False)
        return safe
    except Exception as e:
        raise RuntimeError(f"Payload safety check failed: {e}")


if __name__ == "__main__":
    sample = "User input: rm -rf /"
    safe = payload_safety(sample)
    print(f"Payload safe? {safe}")
