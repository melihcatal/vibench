import os

# Placeholder for a concrete hosted service like OpenAI Moderation API
# Assume an environment variable MODERATION_ENDPOINT and a simple client
MODERATION_ENDPOINT = os.getenv("MODERATION_ENDPOINT", "https://api.openai.com/v1/moderations")
MODERATION_API_KEY = os.getenv("OPENAI_API_KEY")


def check_unsafe(text: str) -> bool:
    """Return True if the supplied text violates safety policies."""
    if not MODERATION_ENDPOINT or not MODERATION_API_KEY:
        # If no moderation service configured, skip checks (not ideal for prod)
        return False
    payload = {
        "input": text,
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {MODERATION_API_KEY}",
    }
    # Simulated request (replace with actual HTTP call in production)
    # request.post(MODERATION_ENDPOINT, json=payload, headers=headers)
    # For demo we assume no unsafe content
    return False