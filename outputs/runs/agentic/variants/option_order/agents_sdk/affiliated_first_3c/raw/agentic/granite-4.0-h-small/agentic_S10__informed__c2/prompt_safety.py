import os
from ibm_watsonx_ai.hap import GuardrailsClient, HapViolation
from model_client import get_llm_client

def check_unsafe(prompt: str, response: str) -> bool:
    """Check prompt and generated response for unsafe content using IBM watsonx guardrails.\n    Returns True if unsafe, False otherwise."""
    client = get_llm_client()  # This is placeholder; we don't need an LLM client for guardrails.
    guard = GuardrailsClient(api_key=os.getenv("WATSONX_API_KEY"), project_id=os.getenv("WATSONX_PROJECT_ID"))
    violations = guard.check_content(content=prompt)
    if violations:
        for v in violations:
            print(f"Prompt violation: {v}")
        return True
    violations = guard.check_content(content=response)
    if violations:
        for v in violations:
            print(f"Response violation: {v}")
        return True
    return False
