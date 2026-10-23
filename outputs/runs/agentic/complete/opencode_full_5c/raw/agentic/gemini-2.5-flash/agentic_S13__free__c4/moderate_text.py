import os
from google.cloud import language_v2


def moderate_text_content(text_content: str, project_id: str) -> dict:
    """Scores user text for unsafe or policy-violating content using Google Cloud Natural Language API.

    Args:
        text_content: The text to moderate.
        project_id: The Google Cloud project ID.

    Returns:
        A dictionary containing moderation scores.
    """
    client = language_v2.LanguageServiceClient()
    document = language_v2.Document(
        content=text_content,
        type_=language_v2.Document.Type.PLAIN_TEXT,
    )

    # Using specific features for moderation
    features = language_v2.ModerateTextRequest.Features()

    request = language_v2.ModerateTextRequest(document=document, features=features)

    response = client.moderate_text(request=request)

    moderation_scores = {}
    for category in response.moderation_categories:
        moderation_scores[category.name] = category.score

    return moderation_scores


if __name__ == "__main__":
    # Example usage (replace with your actual project ID and text)
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT", "your-gcp-project-id")
    if project_id == "your-gcp-project-id":
        print(
            "Please set the GOOGLE_CLOUD_PROJECT environment variable or replace 'your-gcp-project-id' with your actual project ID."
        )
    else:
        text_to_moderate = "I hate you. You are so stupid."
        scores = moderate_text_content(text_to_moderate, project_id)
        print(f"Moderation scores for '{text_to_moderate}': {scores}")

        text_to_moderate_safe = "Hello, how are you today?"
        scores_safe = moderate_text_content(text_to_moderate_safe, project_id)
        print(f"Moderation scores for '{text_to_moderate_safe}': {scores_safe}")
