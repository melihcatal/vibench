from safety_client import ContentSafetyClient
from safety_models import ModerationRequest, ModerationResult, ModerationResultCategory
from google.cloud import content_safety_v1


def moderate_text(request: ModerationRequest) -> ModerationResult:
    client_wrapper = ContentSafetyClient()
    client = client_wrapper.get_client()
    project_id = client_wrapper.get_project_id()
    location = client_wrapper.get_location()

    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT_ID environment variable not set.")

    parent = f"projects/{project_id}/locations/{location}"

    # Construct the request for the Google Cloud Content Safety API
    detection_request = content_safety_v1.AnnotateTextRequest(
        parent=parent,
        text_content=request.text,
    )

    response = client.annotate_text(detection_request)

    blocked = False
    categories = []
    for category_detection in response.moderation_categories_findings:
        category_name = content_safety_v1.HarmCategory(category_detection.category).name
        severity = category_detection.severity
        categories.append(
            ModerationResultCategory(category=category_name, severity=severity)
        )
        # Decide if blocked based on severity (e.g., severity > 0 means some level of harm detected)
        if severity > 0:
            blocked = True

    return ModerationResult(
        blocked=blocked,
        categories=categories,
        raw_response=content_safety_v1.AnnotateTextResponse.to_dict(
            response
        ),  # Convert to dict for raw_response
    )
