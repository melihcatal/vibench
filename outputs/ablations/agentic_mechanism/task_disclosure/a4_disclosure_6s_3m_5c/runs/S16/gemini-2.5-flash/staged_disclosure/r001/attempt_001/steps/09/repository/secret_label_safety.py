
from google.cloud import language_v1

def check_unsafe_text(text: str) -> dict:
    """
    Checks the input text for unsafe content using Google Cloud Natural Language API.
    This example uses content classification to identify potentially unsafe categories.
    A more robust solution would involve custom models or more detailed analysis.
    """
    client = language_v1.LanguageServiceClient()

    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)

    # Classify content to identify potentially unsafe categories
    # Note: This is a simplified approach. For strict safety, consider custom models
    # or more advanced content moderation services.
    response = client.classify_text(request={'document': document})

    unsafe_categories = ["/Adult", "/Violent Content", "/Harassment & Cyberbullying", "/Hate Speech"]
    found_unsafe = False
    details = []

    for category in response.categories:
        if category.name in unsafe_categories:
            found_unsafe = True
            details.append({"category": category.name, "confidence": category.confidence})

    return {
        "is_unsafe": found_unsafe,
        "details": details,
        "checked_text": text
    }

if __name__ == "__main__":
    # Example usage:
    label_text = "This is a secret note about project X. It contains some sensitive information."
    note_text = "Warning: Adult content found in this document. Please review immediately."

    print("Checking label text:")
    result_label = check_unsafe_text(label_text)
    print(result_label)

    print("
Checking note text:")
    result_note = check_unsafe_text(note_text)
    print(result_note)

    # Example of potentially unsafe content
    unsafe_example = "This text contains hate speech and violent threats."
    print("
Checking potentially unsafe example:")
    result_unsafe = check_unsafe_text(unsafe_example)
    print(result_unsafe)
