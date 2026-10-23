import os
from google.cloud import language_v1

def moderate_document_text(text_content: str) -> dict:
    """
    Checks extracted document text for unsafe content using Google Cloud Natural Language API.

    Args:
        text_content: The text extracted from the document.

    Returns:
        A dictionary containing the moderation results.
    """
    client = language_v1.LanguageServiceClient()

    document = language_v1.Document(content=text_content, type_=language_v1.Document.Type.PLAIN_TEXT)

    # Available categories: "Toxic", "Spam", "Sexual", "Violent", "Political", "Religion"
    response = client.moderate_text(document=document)

    result = {"moderation_categories": []}
    for category_filter in response.moderation_categories:
        result["moderation_categories"].append(
            {
                "name": category_filter.name,
                "score": category_filter.score,
            }
        )
    return result

if __name__ == "__main__":
    # Example usage:
    # Set the GOOGLE_APPLICATION_CREDENTIALS environment variable
    # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/your/keyfile.json"

    sample_text = "This is a sample text with potentially unsafe content like hate speech."
    moderation_results = moderate_document_text(sample_text)
    print("Moderation Results:")
    for category in moderation_results["moderation_categories"]:
        print(f"  Category: {category['name']}, Score: {category['score']:.4f}")

    sample_text_safe = "This is a perfectly safe document about programming."
    moderation_results_safe = moderate_document_text(sample_text_safe)
    print("
Moderation Results (Safe Text):")
    for category in moderation_results_safe["moderation_categories"]:
        print(f"  Category: {category['name']}, Score: {category['score']:.4f}")
