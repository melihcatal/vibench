from google.cloud import language_v1

def check_unsafe_content(text_payload: str):
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(content=text_payload, type_=language_v1.Document.Type.PLAIN_TEXT)

    # Available categories for content classification
    # See https://cloud.google.com/natural-language/docs/reference/rest/v1/documents/analyzeContent
    response = client.classify_text(request={'document': document})

    # You can customize the logic to determine what constitutes "unsafe" based on your needs
    # For example, checking for specific categories or confidence scores
    for category in response.categories:
        if "Violence" in category.name or "Sexual" in category.name or "Hate Speech" in category.name:
            if category.confidence > 0.5:  # Example threshold
                return True, f"Unsafe content detected in category: {category.name} with confidence: {category.confidence}"
    
    return False, "No unsafe content detected."

