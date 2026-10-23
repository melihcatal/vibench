# vendor_text_safety.py
# [LATER-STEP]
# Moderate vendor notes or memo fields using watsonx Guardrails / HAP detection.

import json
from ibm_watsonx_ai import APIClient
from ibm_watsonx_ai.hap import HarmDetectionModel, HarmCategory
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

# Authenticate using the watsonx API key
authenticator = IAMAuthenticator(os.getenv("WATSONX_API_KEY"))
client = APIClient(
    authenticator=authenticator, service_instance_id=os.getenv("WATSONX_PROJECT_ID")
)
model = HarmDetectionModel(client=client)


def moderate_vendor_notes(notes: str) -> Dict[str, Any]:
    """Run watsonx guardrails on vendor notes and return safety result.

    Args:
        notes: Free‑text memo/narrative supplied by the vendor.

    Returns:
        A dict with keys:
          - safe: bool (True if acceptable)
          - violations: list of detected harm categories
    """
    # Submit the notes to guardrails model
    response = model.detect_harm(
        text=notes,
        categories=[HarmCategory.HATE, HarmCategory.SEXUAL, HarmCategory.VIOLENCE],
    )
    # Process response (simplified)
    violations = [cat.value for cat in response.categories if cat.is_detected]
    safe = len(violations) == 0
    return {"safe": safe, "violations": violations}


# Example usage
if __name__ == "__main__":
    notes_txt = "This invoice includes premium services which may be controversial.\nPlease confirm the vendor's licensing status before payment."
    result = moderate_vendor_notes(notes_txt)
    print(json.dumps(result, indent=2))
