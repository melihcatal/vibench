from google.cloud import language_v1

def check_platform_output_safety(text_content: str):
    """Checks Google Vertex AI platform model output for unsafe content using Google Cloud Natural Language API."""
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(
        content=text_content, type_=language_v1.Document.Type.PLAIN_TEXT
    )
    
    # Classify text content for categories that might indicate unsafe content
    # Note: For more robust safety, consider Perspective API or a dedicated moderation service.
    response = client.classify_text(request={'document': document})
    
    # This is a simplified example. You would typically define thresholds and specific categories
    # to determine if content is 'unsafe'.
    # For demonstration, we'll just return the categories found.
    categories = [category.name for category in response.categories]
    
    return {"text": text_content, "safety_categories": categories}
