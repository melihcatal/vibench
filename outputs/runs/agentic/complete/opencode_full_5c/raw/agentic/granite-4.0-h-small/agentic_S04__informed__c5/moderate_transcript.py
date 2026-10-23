# [LATER-STEP] moderate_transcript.py
# Moderate transcript text using watsonx.ai guardrails (HAP detection) SDK
import os
from ibm_watsonx_ai import Client
from ibm_watsonx_ai.consts import EndpointID
from speech_client import get_auth_header

WATSONX_API_KEY = os.getenv("WATSONX_API_KEY")
WATSONX_PROJECT_ID = os.getenv("WATSONX_PROJECT_ID")
ENDPOINT_ID = EndpointID.HAP_DETECTION  # Guardrails / HAP detection endpoint

client = Client(
    authenticator=Client.IAMAuthenticator(api_key=WATSONX_API_KEY),
    project_id=WATSONX_PROJECT_ID,
)


def moderate_text(text: str) -> bool:
    """
    Run the provided transcript through watsonx guardrails.
    Returns True if the content is considered safe, False otherwise.
    """
    response = client.content_moderation.analyze_text(
        text=text, endpoint_id=ENDPOINT_ID
    )
    result = response.get_result()
    # Sample result: {"moderation_labels": [{"label": "Hate", "severity": "High"}], "input_text": ...}
    # If any high-severity label is present, treat as unsafe
    for label in result.get("moderation_labels", []):
        if label.get("severity", "Low") in ("High", "Moderate"):
            return False
    return True


if __name__ == "__main__":
    import sys, json

    if len(sys.argv) != 2:
        print("Usage: python moderate_transcript.py <path-to-json-transcript>")
        sys.exit(1)
    with open(sys.argv[1], "r") as f:
        payload = json.load(f)
    text = payload.get("text", payload.get("transcript", ""))
    is_safe = moderate_text(text)
    print("Transcript safe for publishing?", is_safe)
