# metric_annotation_safety.py
# LATER-STEP: Check free‑text metric labels or annotations for unsafe content

from observability_client import ObservabilityClient
from observability_models import SafetyRequest, SafetyResponse


def check_label_safety(text: str, context: dict = None) -> SafetyResponse:
    """Determine whether a label/annotation string contains unsafe language.

    The function forwards the text to a text‑moderation service and returns a
    boolean flag plus optional details.

    Args:
        text: The raw label or annotation string to evaluate.
        context: Optional additional context (e.g., label key, resource type)
                 that can be passed to the moderation endpoint.

    Returns:
        SafetyResponse with `flag=True` if unsafe content is detected.
    """
    client = ObservabilityClient()

    # Example: call a provider‑agnostic moderation endpoint via HTTP
    # In this example we use the generic request/response helpers; replace
    # with the actual moderation provider SDK when integrated.
    payload = SafetyRequest(text=text, context=context or {})
    resp = client.request("POST", "/moderation/label", json=payload.to_dict())
    # Normalize response: provider may return {"flag": true, "details": {...}}
    return SafetyResponse(**resp)


# Example usage for local verification
if __name__ == "__main__":
    unsafe = check_label_safety(
        text="Disk usage on /dev/sda exceeds threshold!!!",
        context={"label": "alert_message"},
    )
    print("Unsafe flag:", unsafe.flag)
    if unsafe.flag:
        print("Details:", unsafe.details)
