from safety_client import ContentSafetyClient
from safety_models import ModerationRequest, RedactionResult, ModerationResultCategory
from google.cloud import content_safety_v1


def redact_unsafe(request: ModerationRequest) -> RedactionResult:
    client_wrapper = ContentSafetyClient()
    client = client_wrapper.get_client()
    project_id = client_wrapper.get_project_id()
    location = client_wrapper.get_location()

    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT_ID environment variable not set.")

    parent = f"projects/{project_id}/locations/{location}"

    # Construct the request for the Google Cloud Content Safety API with redaction
    detection_request = content_safety_v1.AnnotateTextRequest(
        parent=parent,
        text_content=request.text,
        # Enable redaction by adding a TextDetectionAction with redaction
        text_detection_actions=[
            content_safety_v1.AnnotateTextRequest.TextDetectionAction(
                redaction=content_safety_v1.Redaction()
            )
        ],
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
        if severity > 0:
            blocked = True

    redacted_text = (
        response.redaction_findings[0].redacted_content
        if response.redaction_findings
        else request.text
    )

    return RedactionResult(
        redacted_text=redacted_text,
        blocked=blocked,
        categories=categories,
        raw_response=content_safety_v1.AnnotateTextResponse.to_dict(response),
    )
