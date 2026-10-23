import os
from google.cloud import aiplatform


def check_content_safety(text: str):
    """
    Checks message payload text for unsafe content using Google Vertex AI.
    """
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

    aiplatform.init(project=project_id, location="us-central1")

    from vertexai.preview.language_models import TextModerationModel

    model = TextModerationModel.from_pretrained("text-moderation@001")

    response = model.moderate_text(text)

    return response


if __name__ == "__main__":
    # This is an example, and will not be executed.
    unsafe_text = "I am going to do something violent"
    safety_ratings = check_content_safety(unsafe_text)
    print(f"Safety ratings for unsafe text: {safety_ratings}")

    safe_text = "This is a perfectly normal and safe message."
    safety_ratings_safe = check_content_safety(safe_text)
    print(f"Safety ratings for safe text: {safety_ratings_safe}")
