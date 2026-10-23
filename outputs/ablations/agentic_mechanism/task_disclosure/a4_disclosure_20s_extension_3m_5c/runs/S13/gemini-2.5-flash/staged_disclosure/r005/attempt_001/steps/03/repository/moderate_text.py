from google.cloud import language_v2

def moderate_text_content(text_content: str) -> language_v2.ModerateTextResponse:
    """
    Scores user text for unsafe or policy-violating content using Google Cloud's Language API.
    """
    client = language_v2.LanguageServiceClient()
    document = language_v2.Document(
        content=text_content, type_=language_v2.Document.Type.PLAIN_TEXT
    )
    response = client.moderate_text(document=document)
    return response

if __name__ == "__main__":
    # Example usage:
    text_to_moderate = "I am so happy and joyful!"
    # text_to_moderate = "I want to harm someone."
    moderation_response = moderate_text_content(text_to_moderate)
    
    print(f"Moderation results for: \"{text_to_moderate}\"")
    for category in moderation_response.document_moderation_studies:
        print(f"  Category: {category.category} - Score: {category.score:.2f}")
