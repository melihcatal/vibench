from google.cloud import language_v1
import os

GOOGLE_CLOUD_PROJECT = os.environ.get("GOOGLE_CLOUD_PROJECT")

def profile_moderation(text):
    client = language_v1.LanguageServiceClient(project=GOOGLE_CLOUD_PROJECT)
    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
    # Classify content to check for policy violations or inappropriate text
    # For a more robust moderation, consider using the Moderation API or a custom model
    response = client.classify_text(request={'document': document})
    # This is a basic example; actual moderation would involve analyzing categories and confidence scores.
    # For simplicity, we'll just return the categories found.
    categories = [category.name for category in response.categories]
    return {"moderation_categories": categories}
