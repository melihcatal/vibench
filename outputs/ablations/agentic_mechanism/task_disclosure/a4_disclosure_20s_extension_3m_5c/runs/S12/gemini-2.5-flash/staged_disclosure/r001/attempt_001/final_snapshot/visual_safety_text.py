
from google.cloud import language_v1

def check_unsafe_text(text_content: str):
    """
    Checks the given text content for unsafe text using Google Cloud Natural Language API.
    """
    client = language_v1.LanguageServiceClient()

    document = language_v1.Document(
        content=text_content, type_=language_v1.Document.Type.PLAIN_TEXT
    )

    # Available categories: https://cloud.google.com/natural-language/docs/moderating-text
    response = client.moderate_text(document=document)

    safety_labels = []
    for category_filter in response.moderation_categories:
        safety_labels.append(
            {
                "category": category_filter.name,
                "score": category_filter.score,
            }
        )
    return safety_labels

if __name__ == "__main__":
    # Example usage:
    text_to_check = "This is an example text with some potentially unsafe content like hate speech."
    results = check_unsafe_text(text_to_check)
    print(results)
