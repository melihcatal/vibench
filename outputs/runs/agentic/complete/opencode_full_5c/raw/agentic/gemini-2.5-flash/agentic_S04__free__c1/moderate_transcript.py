import os
from google.cloud import language_v1

def moderate_text(project_id: str, text_content: str):
    """Moderates transcript text using Google Cloud Natural Language API.

    Args:
        project_id: The Google Cloud project ID.
        text_content: The text content to moderate.

    Returns:
        A dictionary containing moderation categories and their confidence scores.
    """
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(content=text_content, type_=language_v1.Document.Type.PLAIN_TEXT)

    # Available categories can be found here:
    # https://cloud.google.com/natural-language/docs/reference/rest/v1/projects.documents/annotateText#moderate_text_detection_model
    response = client.moderate_text(document=document)

    moderation_results = {}
    for category in response.moderation_categories:
        moderation_results[category.name] = category.confidence
    return moderation_results

if __name__ == "__main__":
    # Example usage
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    transcript_text = "This is a clean sentence. However, this sentence contains some potentially inappropriate language like cursing and offensive remarks."

    if project_id:
        print(f"Moderating text: "{transcript_text}"")
        results = moderate_text(project_id, transcript_text)
        print("Moderation Results:")
        for category, confidence in results.items():
            print(f"- {category}: {confidence:.2f}")
    else:
        print("GOOGLE_CLOUD_PROJECT environment variable not set.")
