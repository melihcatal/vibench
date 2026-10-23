from google.cloud import language_v1

def check_text_safety(text_content: str):
    """
    Checks user-generated text content for unsafe content using Google Cloud Natural Language API.

    Args:
        text_content: The string content to analyze.

    Returns:
        A list of content classifications from the Natural Language API.
    """
    client = language_v1.LanguageServiceClient()

    document = language_v1.Document(
        content=text_content, type_=language_v1.Document.Type.PLAIN_TEXT
    )

    # Classify content to identify categories that might be considered unsafe
    # For more granular safety checks (e.g., toxicity), consider using Google Cloud's
    # Perspective API or Generative AI Safety features.
    response = client.classify_text(request={"document": document})
    
    return response.categories

if __name__ == "__main__":
    # Example usage
    unsafe_text = "I hate you. You are terrible."
    safe_text = "This is a wonderful day filled with joy and happiness."

    print(f"Safety check for '{unsafe_text}':")
    unsafe_categories = check_text_safety(unsafe_text)
    for category in unsafe_categories:
        print(f"  Category: {category.name}, Confidence: {category.confidence:.2f}")

    print(f"\nSafety check for '{safe_text}':")
    safe_categories = check_text_safety(safe_text)
    for category in safe_categories:
        print(f"  Category: {category.name}, Confidence: {category.confidence:.2f}")
