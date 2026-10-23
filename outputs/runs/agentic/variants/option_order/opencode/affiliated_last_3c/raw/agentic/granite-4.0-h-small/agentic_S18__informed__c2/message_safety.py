# message_safety.py
# LATER-STEP: Detect unsafe content in message payloads

import os
from typing import Optional, Dict, Any
from messaging_models import Event, ErrorResponse

# Choose a content safety service based on env variable
SAFETY_SERVICE = os.getenv("CONTENT_SAFETY_PROVIDER", "perspective")

# Mapping of supported providers to importable modules
# NOTE: These imports are placeholder skeletons for illustration.
# In production you would install the required SDK or use a requests wrapper.
if SAFETY_SERVICE == "perspective":
    # Placeholder for Perspective API client (REST)
    from .safety_providers import perspective_client as safety_client
elif SAFETY_SERVICE == "alibaba":
    # Placeholder for Alibaba Cloud Content Moderation SDK
    from .safety_providers import alibaba_moderation as safety_client
else:
    # Fallback to a dummy implementation that always marks content safe
    def check(text: str) -> Optional[Dict[str, Any]]:
        return None

    safety_client = type("Dummy", (), {"check": staticmethod(check)})


def scan_payload(event: Event) -> Optional[ErrorResponse]:
    """Inspect the event data field for unsafe content.

    Returns an ErrorResponse if unsafe text is found, otherwise None.
    """
    unsafe = safety_client.check(event.data.get("text", ""))
    if unsafe:
        return ErrorResponse(
            code="UNSAFE_CONTENT",
            message="Message contains unsafe content",
            details={"safetyCheck": unsafe},
        )
    return None


# Placeholder implementations for illustration
# In a real repo, you would place these in a separate module under ./safety_providers/
# Example skeleton for Alibaba:
# def alibaba_moderation.check(text: str) -> Optional[Dict[str, Any]]:
#     ... call Alibaba API ...

# Example skeleton for Perspective:
# def perspective_client.check(text: str) -> Optional[Dict[str, Any]]:
#     ... POST to https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze ...

if __name__ == "__main__":
    # Simple demo using the placeholder safe implementation
    ev = Event(
        event_id="test-001",
        data={"text": "This is safe."},
        timestamp="2025-08-01T12:00:00Z",
    )
    result = scan_payload(ev)
    print("Safety check result:", result)
