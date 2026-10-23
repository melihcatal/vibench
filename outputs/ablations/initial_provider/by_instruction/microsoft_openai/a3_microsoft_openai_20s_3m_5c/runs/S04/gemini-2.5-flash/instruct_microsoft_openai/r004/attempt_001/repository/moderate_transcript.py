from google.cloud import language_v1
import os

def moderate_text(text_content: str) -> dict:
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.environ.get("GOOGLE_NATURAL_LANGUAGE_CREDENTIALS_PATH")
    if not os.environ.get("GOOGLE_NATURAL_LANGUAGE_CREDENTIALS_PATH"):
        raise ValueError("GOOGLE_NATURAL_LANGUAGE_CREDENTIALS_PATH environment variable must be set.")

    client = language_v1.LanguageServiceClient()

    document = language_v1.Document(content=text_content, type_=language_v1.Document.Type.PLAIN_TEXT)

    # Available categories: https://cloud.google.com/natural-language/docs/categories
    response = client.classify_text(request={\"document\": document})

    moderation_results = []
    for category in response.categories:
        moderation_results.append({
            \"name\": category.name,
            \"confidence\": category.confidence,
        })

    return {\"categories\": moderation_results}
