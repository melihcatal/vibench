# platform_output_safety.py
# Managed Model Platform Workflow: check model output for unsafe content
# Provider: watsonx.ai guardrails (IBM watsonx.ai)
import os
import ibm_watsonx_ai
from ibm_watsonx_ai.nlp.guardrails import GuardrailsService
from ibm_watsonx_ai.auth import TrustTokenAuth

# Load credentials from environment variables
WATSONX_API_KEY = os.getenv("WATSONX_API_KEY")
WATSONX_PROJECT_ID = os.getenv("WATSONX_PROJECT_ID")

guardrails = GuardrailsService(auth=TrustTokenAuth(bearer_token=WATSONX_API_KEY), project_id=WATSONX_PROJECT_ID)

def check_output_for_unsafe(content: str) -> dict:
    """Run IBM watsonx.ai guardrails analysis on provided text.

    Returns a dict with keys:
        - 'is_safe': bool indicating safety
        - 'issues': list of detected issues (if any)
        - 'raw': raw guardrails JSON response
    """
    response = guardrails.analyze(content=content)
    # Guardrails returns a list of issues; empty list means safe
    issues = response.get("issues", [])
    is_safe = len(issues) == 0
    return {
        "is_safe": is_safe,
        "issues": issues,
        "raw": response,
    }

if __name__ == "__main__":
    # Example usage with safety check
    test_text = "Be sure to download this malicious file from http://bad.example.com"
    result = check_output_for_unsafe(test_text)
    print(result)
