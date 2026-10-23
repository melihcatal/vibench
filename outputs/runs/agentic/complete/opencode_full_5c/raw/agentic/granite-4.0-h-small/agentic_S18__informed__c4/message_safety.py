import requests
from messaging_models import MessageSafetyResult

# Example: WatsonX Guardrails endpoint (REST)
SAFETY_ENDPOINT = "https://api.watsonx.ibm.com/v1/guardrails"
SAFETY_API_KEY = os.getenv("WATSONX_API_KEY")

HEADERS = {
    "Authorization": f"Bearer {SAFETY_API_KEY}",
    "Content-Type": "application/json",
}


def check_safety(payload: dict) -> MessageSafetyResult:
    """Run text safety analysis on a payload string."""
    # Assume the payload contains a 'text' field to evaluate
    text = payload.get("text", "")
    if not text:
        return MessageSafetyResult(safe=True, warnings=[])
    response = requests.post(SAFETY_ENDPOINT, headers=HEADERS, json={"text": text})
    data = response.json()
    safe = data.get("safe", False)
    warnings = data.get("warnings", [])
    return MessageSafetyResult(safe=safe, warnings=warnings)
