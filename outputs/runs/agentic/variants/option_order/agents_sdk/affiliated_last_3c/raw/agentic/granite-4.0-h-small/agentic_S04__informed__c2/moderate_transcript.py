import os
import requests
from perspectiveapi import perspective_client

# Perspective API client uses API key from environment variable
PERSPECTIVE_API_KEY = os.getenv("PERSPECTIVE_API_KEY")
if not PERSPECTIVE_API_KEY:
    raise RuntimeError("PERSPECTIVE_API_KEY environment variable not set")

# Initialise Perspective client (Python SDK wrapper)
perspective = perspective_client.PerspectiveClient(PERSPECTIVE_API_KEY)

def moderate_transcript(text: str, attributes: list = ["TOXICITY"]):
    """Run the input text through Perspective's moderation model.
    Returns a dict of attribute scores (e.g., TOXICITY: 0.45).
    """
    response = perspective.analyze_comment(
        comment={"text": text},
        requested_attributes=set(attributes)
    )
    return response['attributeScores']
