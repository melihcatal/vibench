from google.cloud import language_v1
from typing import List


def moderate_transcript_text(text: str) -> language_v1.ModerateTextResponse:
    """
    Moderates a given text using Google Cloud Natural Language's moderateText API.
    """
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(
        content=text, type_=language_v1.Document.Type.PLAIN_TEXT
    )

    response = client.moderate_text(document=document)
    return response


if __name__ == "__main__":
    # Example usage
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    transcript_text = (
        "This is some example text which might contain some explicit content."
    )
    moderation_result = moderate_transcript_text(transcript_text)

    print("Moderation categories:")
    for category in moderation_result.moderation_categories:
        print(f"  Category: {category.name}, Confidence: {category.score:.2f}")

    # You can then use the scores to decide if content needs to be flagged or filtered
