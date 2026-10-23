import os
from google.cloud import language_v2

def check_unsafe_content(text_content: str) -> dict:
    """
    Checks extracted document text for unsafe content using Google Cloud Language AI.

    Args:
        text_content: The text extracted from the document.

    Returns:
        A dictionary containing the moderation result.
    """
    client = language_v2.LanguageServiceClient()

    document = language_v2.Document(
        content=text_content, type_=language_v2.Document.Type.PLAIN_TEXT
    )

    # Perform content moderation
    response = client.moderate_text(document=document)

    result = {}
    for category_score in response.moderation_categories:
        result[category_score.name] = category_score.score

    return result

if __name__ == "__main__":
    # Example usage (replace with actual extracted text)
    sample_text = "This is some sample text that might contain unsafe content like hate speech."
    
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    # For local testing, you might need to set up authentication, e.g.:
    # export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/keyfile.json"

    if "GOOGLE_APPLICATION_CREDENTIALS" not in os.environ:
        print("Error: GOOGLE_APPLICATION_CREDENTIALS environment variable not set.")
        print("Please set it to the path of your Google Cloud service account key file.")
    else:
        print(f"Checking text for unsafe content: \"{sample_text}\"")
        moderation_results = check_unsafe_content(sample_text)
        print("Moderation Results:")
        for category, score in moderation_results.items():
            print(f"- {category}: {score:.4f}")
