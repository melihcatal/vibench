import os
from typing import List
from google.cloud import contentmoderation_v3
from security_models import ModerationResult, ModerationCategory

def check_secret_label_safety(text_content: str, project_id: str = None) -> ModerationResult:
    if project_id is None:
        project_id = os.getenv("GCP_PROJECT_ID")
    if not project_id:
        raise ValueError("GCP_PROJECT_ID not provided and not found in environment variables.")

    client = contentmoderation_v3.ContentModerationServiceClient()
    parent = f"projects/{project_id}/locations/global"

    try:
        request = contentmoderation_v3.ModerateTextRequest(
            parent=parent,
            content=text_content,
        )
        response = client.moderate_text(request=request)

        categories: List[ModerationCategory] = []
        has_unsafe_content = False

        for detection_category in response.detections:
            categories.append(ModerationCategory(
                category=detection_category.category,
                score=detection_category.score
            ))
            # A common threshold for 'unsafe' is a score > 0.5
            if detection_category.score > 0.5:
                has_unsafe_content = True

        return ModerationResult(categories=categories, has_unsafe_content=has_unsafe_content)

    except Exception as e:
        raise RuntimeError(f"Error checking secret label safety with Google Content Moderation: {e}")
