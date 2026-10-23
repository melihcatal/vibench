from google.cloud import language_v1

def check_unsafe_content(text_content):
    client = language_v1.LanguageServiceClient()

    document = language_v1.Document(content=text_content, type_=language_v1.Document.Type.PLAIN_TEXT)

    # Available categories: UNSPECIFIED, TOXICITY, SEXUALLY_EXPLICIT, VIOLENCE, RELIGION, INSULT, THREAT, DEROGATORY, HATE_SPEECH, MEDICAL, FINANCE
    # You may need to enable the specific categories in your Google Cloud project.
    response = client.moderate_text(document=document)

    unsafe_categories = []
    for category_filter in response.moderation_categories:
        if category_filter.score > 0.7:  # Adjust threshold as needed
            unsafe_categories.append(category_filter.name)
    
    return unsafe_categories
