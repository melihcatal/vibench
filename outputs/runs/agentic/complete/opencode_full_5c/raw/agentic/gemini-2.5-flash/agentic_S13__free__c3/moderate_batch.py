from safety_client import ContentSafetyClient
from safety_models import (
    BatchModerationRequest,
    BatchModerationResult,
    BatchModerationResultItem,
    ModerationResult,
    ModerationResultCategory,
)
from google.cloud import content_safety_v1


def moderate_batch(request: BatchModerationRequest) -> BatchModerationResult:
    client_wrapper = ContentSafetyClient()
    client = client_wrapper.get_client()
    project_id = client_wrapper.get_project_id()
    location = client_wrapper.get_location()

    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT_ID environment variable not set.")

    parent = f"projects/{project_id}/locations/{location}"

    batch_results = []
    for text in request.texts:
        detection_request = content_safety_v1.AnnotateTextRequest(
            parent=parent,
            text_content=text,
        )
        response = client.annotate_text(detection_request)

        blocked = False
        categories = []
        for category_detection in response.moderation_categories_findings:
            category_name = content_safety_v1.HarmCategory(
                category_detection.category
            ).name
            severity = category_detection.severity
            categories.append(
                ModerationResultCategory(category=category_name, severity=severity)
            )
            if severity > 0:
                blocked = True

        moderation_result = ModerationResult(
            blocked=blocked,
            categories=categories,
            raw_response=content_safety_v1.AnnotateTextResponse.to_dict(response),
        )
        batch_results.append(
            BatchModerationResultItem(
                original_text=text, moderation_result=moderation_result
            )
        )

    return BatchModerationResult(results=batch_results)
