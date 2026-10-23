import os
from ibm_watsonx_ai import APIClient
from ibm_watsonx_ai.hai.content_safety import ModerationServiceV2


def is_unsafe(prompt: str) -> bool:
    """Check a prompt for unsafe content using watsonx guardrails (HAP detection)."""
    api_key = os.getenv("WATSONX_API_KEY", "<INSERT_WATSONX_API_KEY>")
    project_id = os.getenv("WATSONX_PROJECT_ID", "<INSERT_WATSONX_PROJECT_ID>")
    client = APIClient(
        api_key=api_key, project_id=project_id, url="https://api.watsonx.ai"
    )
    moderation = ModerationServiceV2(client)
    # Watsonx expects a list of texts; we pass our prompt as a single-item list.
    response = moderation.moderate_content(input_texts=[prompt])
    # Response shape: [{'result': {'labels': [{'label': 'HAP', 'severity': 'moderate'}]}}]
    for result in response[0].get("result", {}).get("labels", []):
        if result["label"] == "HAP" and result["severity"] in ("moderate", "high"):
            return True
    return False
