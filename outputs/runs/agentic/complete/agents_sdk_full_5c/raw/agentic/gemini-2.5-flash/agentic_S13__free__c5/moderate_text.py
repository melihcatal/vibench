from google.cloud import language_v2

def moderate_text(text: str) -> dict:
    """
    Scores user text for unsafe or policy-violating content using Google Cloud Natural Language API.
    """
    client = language_v2.LanguageServiceClient()
    document = language_v2.Document(content=text, type_=language_v2.Document.Type.PLAIN_TEXT)
    
    # Supported categories for content classification
    # See https://cloud.google.com/natural-language/docs/categories
    response = client.moderate_text(document=document)
    
    # The response contains a list of classifications, each with a category name and confidence score.
    # The categories are general, but can indicate unsafe content types.
    # For more granular safety, a dedicated Content Safety API might be preferred.
    results = []
    for category in response.moderation_categories:
        results.append({
            "category": category.name,
            "confidence": category.confidence
        })
    return {"moderation_results": results}

if __name__ == '__main__':
    example_text = "I hate this! This is really bad content."
    moderation_output = moderate_text(example_text)
    print(f"Moderation results for '{example_text}':")
    for res in moderation_output.get("moderation_results", []):
        print(f"  Category: {res['category']}, Confidence: {res['confidence']:.2f}")

    example_text_safe = "Hello, how are you today?"
    moderation_output_safe = moderate_text(example_text_safe)
    print(f"\nModeration results for '{example_text_safe}':")
    for res in moderation_output_safe.get("moderation_results", []):
        print(f"  Category: {res['category']}, Confidence: {res['confidence']:.2f}")
