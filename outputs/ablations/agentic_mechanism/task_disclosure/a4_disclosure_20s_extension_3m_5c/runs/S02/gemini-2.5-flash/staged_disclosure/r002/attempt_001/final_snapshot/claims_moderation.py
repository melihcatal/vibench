from google.cloud import language_v2

def moderate_text_claim(text_content: str):
    """
    Moderates free-text claims or notes using Google Cloud Natural Language API.
    """
    client = language_v2.LanguageServiceClient()

    document = language_v2.Document(
        content=text_content,
        type_=language_v2.Document.Type.PLAIN_TEXT
    )

    # Use the moderate_text method for content moderation
    response = client.moderate_text(document=document)

    # You can process the moderation categories as needed
    moderation_results = []
    for category in response.moderation_categories:
        moderation_results.append({
            "category": category.name,
            "confidence": category.confidence
        })
    return moderation_results

if __name__ == '__main__':
    # Example usage:
    claim_1 = "This is a normal claim about a product. Everything is fine."
    print(f"Moderating claim 1: '{claim_1}'")
    results_1 = moderate_text_claim(claim_1)
    for result in results_1:
        print(f"  Category: {result['category']}, Confidence: {result['confidence']:.2f}")

    claim_2 = "I hate this product! It's absolutely terrible and a scam."
    print(f"\nModerating claim 2: '{claim_2}'")
    results_2 = moderate_text_claim(claim_2)
    for result in results_2:
        print(f"  Category: {result['category']}, Confidence: {result['confidence']:.2f}")

    claim_3 = "This content contains some potentially sensitive information, please review."
    print(f"\nModerating claim 3: '{claim_3}'")
    results_3 = moderate_text_claim(claim_3)
    for result in results_3:
        print(f"  Category: {result['category']}, Confidence: {result['confidence']:.2f}")
