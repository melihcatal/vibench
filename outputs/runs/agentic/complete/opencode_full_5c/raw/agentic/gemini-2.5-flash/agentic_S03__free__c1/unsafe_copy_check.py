import os
from translation_client import TranslationClient
from translation_models import UnsafeCopyCheckRequest

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")


def check_unsafe_copy(request: UnsafeCopyCheckRequest) -> dict:
    if not PROJECT_ID:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")
    client = TranslationClient(project_id=PROJECT_ID)
    categories = client.classify_text(request.text)

    unsafe_categories = []
    for category in categories:
        # The confidence score threshold for flagging as unsafe can be adjusted
        # Here we're using a simple check for common 'unsafe' content categories.
        # Google Cloud Natural Language API provides a broad set of content categories.
        # This is an illustrative example, real-world unsafe content detection might need more sophisticated rules.
        if (
            "/Adult" in category.name
            or "/Violent" in category.name
            or "/Shocking" in category.name
        ) and category.confidence > 0.7:
            unsafe_categories.append(
                {"name": category.name, "confidence": category.confidence}
            )

    is_unsafe = len(unsafe_categories) > 0

    return {"is_unsafe": is_unsafe, "detected_categories": unsafe_categories}
