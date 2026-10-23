from google.cloud import language_v1
import os

def check_unsafe_content(text: str):
    """
    Checks narration scripts for unsafe content using Google Cloud Natural Language API.
    """
    client = language_v1.LanguageServiceClient()

    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)

    # Available categories can be found here:
    # https://cloud.google.com/natural-language/docs/categories
    response = client.classify_text(request={"document": document})

    unsafe_categories = [
        "Adult",
        "Violence",
        "Hate speech",
        "Harassment",
        "Sexual content",
        "Dangerous content"
    ]

    found_unsafe_categories = []
    for category in response.categories:
        # The API returns a confidence score for each category.
        # We can define a threshold for what we consider "unsafe".
        # For simplicity, we'll just check if any of our predefined unsafe categories are present.
        if category.name.lstrip("/").split("/")[0] in unsafe_categories and category.confidence > 0.5:
            found_unsafe_categories.append(category.name)

    if found_unsafe_categories:
        return f"Unsafe content detected in categories: {", ".join(found_unsafe_categories)}"
    else:
        return "No unsafe content detected."

