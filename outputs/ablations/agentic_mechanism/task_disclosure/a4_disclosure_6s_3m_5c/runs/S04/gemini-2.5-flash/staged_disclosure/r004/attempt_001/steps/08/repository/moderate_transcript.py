from google.cloud import language_v1

def moderate_text(text_content):
    client = language_v1.LanguageServiceClient()

    document = language_v1.Document(content=text_content, type_=language_v1.Document.Type.PLAIN_TEXT)

    # Available categories: "Toxic", "Sexual", "Violent", "Political", "Religious", "Health", "Legal", "Finance"
    # See https://cloud.google.com/natural-language/docs/reference/rest/v1/projects.documents/annotateText
    response = client.moderate_text(document=document)

    moderation_results = []
    for category_score in response.moderation_categories:
        moderation_results.append({
            "category": category_score.name,
            "score": category_score.score
        })
    return moderation_results

if __name__ == '__main__':
    # Example usage
    transcript = "This is a test transcript with some potentially harmful content. I hate you."
    results = moderate_text(transcript)
    print(results)
