from google.cloud import language_v1

def moderate_text_safety(text_content):
    """
    Moderates vendor notes or memo fields for safety using Google Cloud Natural Language API.
    """
    client = language_v1.LanguageServiceClient()

    document = language_v1.Document(content=text_content, type_=language_v1.Document.Type.PLAIN_TEXT)

    # Classify content to identify potentially unsafe categories
    response = client.classify_text(request={"document": document})

    safety_issues = []
    for category in response.categories:
        # Google Cloud Natural Language API provides a hierarchy of categories.
        # We can look for categories that might indicate unsafe content.
        # This is a simplified example; a real-world scenario might involve
        # more sophisticated analysis or specific safety APIs.
        if "Violent" in category.name or "Hate speech" in category.name or "Sexual" in category.name:
            safety_issues.append(category.name)

    if safety_issues:
        return f"Potential safety issues detected: {', '.join(safety_issues)}"
    else:
        return "No explicit safety issues detected."

if __name__ == '__main__':
    # Example usage:
    vendor_note_1 = "This is a regular vendor note about delivery."
    vendor_note_2 = "Urgent: Customer complained about a very violent incident."
    vendor_note_3 = "The meeting was productive and everyone agreed."

    print(f"Note 1: {moderate_text_safety(vendor_note_1)}")
    print(f"Note 2: {moderate_text_safety(vendor_note_2)}")
    print(f"Note 3: {moderate_text_safety(vendor_note_3)}")
