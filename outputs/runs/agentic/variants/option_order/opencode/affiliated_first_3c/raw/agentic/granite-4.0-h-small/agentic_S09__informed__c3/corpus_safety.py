import os
import json
from ibm_watsonx_ai.services import ContentSafetyService


def check_corpus_safety(text: str) -> bool:
    """Check whether a corpus text complies with safety requirements using IBM guardrails.

    Returns True if safe, False otherwise.
    """
    api_key = os.getenv("WATSONX_API_KEY")
    project_id = os.getenv("WATSONX_PROJECT_ID")
    if not api_key or not project_id:
        raise RuntimeError(
            "Set WATSONX_API_KEY and WATSONX_PROJECT_ID environment variables"
        )

    client = ContentSafetyService(api_key=api_key, project_id=project_id)
    response = client.analyze(text=text)
    # Example safety flag in response: response.get('safe') == True
    return response.get("safe", False)
