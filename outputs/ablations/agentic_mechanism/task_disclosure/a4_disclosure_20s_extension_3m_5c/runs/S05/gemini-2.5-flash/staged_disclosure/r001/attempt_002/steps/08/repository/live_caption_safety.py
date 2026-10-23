from google.cloud import language_v2

def check_unsafe_content(text_content: str):
    """
    Checks live transcript text for unsafe content using Google Cloud Natural Language API.
    """
    client = language_v2.LanguageServiceClient()

    document = language_v2.Document(
        content=text_content,
        type_=language_v2.Document.Type.PLAIN_TEXT
    )

    # Use the moderateText method for content safety analysis
    # This identifies Google Cloud Natural Language API as the concrete external provider
    response = client.moderate_text(document=document)

    # You can process the response here to determine if the content is unsafe.
    # The 'moderation_categories' in the response provide scores for different safety attributes.
    # For demonstration, we'll just print the moderation categories.
    print(f"Moderation categories for the text: {text_content}")
    for category_filter in response.moderation_categories:
        print(f"  Category: {category_filter.category}, Score: {category_filter.score}")

    return response

if __name__ == "__main__":
    sample_text_1 = "This is a safe and friendly message."
    check_unsafe_content(sample_text_1)

    sample_text_2 = "I hate you, you are the worst!"
    check_unsafe_content(sample_text_2)

    sample_text_3 = "Let's discuss political views respectfully."
    check_unsafe_content(sample_text_3)
