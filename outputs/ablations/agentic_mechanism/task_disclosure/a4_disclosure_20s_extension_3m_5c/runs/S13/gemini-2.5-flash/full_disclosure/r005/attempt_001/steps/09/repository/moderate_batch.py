import os
from google.cloud import content_safety_v1beta1

def moderate_batch(messages: list[str]) -> list[dict]:
    """
    Moderates a batch of user messages and returns per-message decisions.

    Args:
        messages: A list of user messages (strings) to moderate.

    Returns:
        A list of dictionaries, where each dictionary contains the moderation
        decision for a corresponding message.
    """
    client = content_safety_v1beta1.ContentSafetyServiceClient()
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")

    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

    results = []
    for message in messages:
        request = content_safety_v1beta1.AnnotateTextRequest(
            parent=f"projects/{project_id}",
            text_content=message,
        )
        response = client.annotate_text(request=request)
        # Process the response to extract relevant moderation decisions
        # For simplicity, we'll return the full response for each message.
        # In a real application, you might parse `response.safety_ratings`
        # and `response.moderation_categories` to create a more concise decision.
        results.append({"message": message, "moderation_response": response.to_dict()})
    return results
