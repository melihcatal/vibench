import os
from google.cloud import language_v1


def check_content_safety(text: str, project_id: str):
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(
        content=text, type_=language_v1.Document.Type.PLAIN_TEXT
    )

    response = client.moderate_text(request={"document": document})

    unsafe_categories = [
        category.name
        for category in response.moderation_categories
        if category.confidence > 0.7
    ]

    if unsafe_categories:
        print(f"Unsafe content detected in categories: {', '.join(unsafe_categories)}")
        return False, unsafe_categories
    else:
        print("Content is safe.")
        return True, []


if __name__ == "__main__":
    gcp_project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not gcp_project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

    safe_text = "This is a friendly message."
    check_content_safety(safe_text, gcp_project_id)

    unsafe_text = "I am going to make a violent threat."
    check_content_safety(unsafe_text, gcp_project_id)
