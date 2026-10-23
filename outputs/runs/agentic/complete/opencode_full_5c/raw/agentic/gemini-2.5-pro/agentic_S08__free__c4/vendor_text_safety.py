import os
from google.cloud import language_v1
from document_models import SafetyResult


def vendor_text_safety(text: str) -> SafetyResult:
    """
    Moderates vendor notes or memo fields using Google Cloud Natural Language API.
    """
    client = language_v1.LanguageServiceClient()

    document = language_v1.Document(
        content=text, type_=language_v1.Document.Type.PLAIN_TEXT
    )

    response = client.classify_text(document=document)

    categories = {
        category.name: category.confidence for category in response.categories
    }

    # Define "unsafe" categories
    unsafe_categories = [
        "/Adult",
        "/Sensitive Subjects",
        "/Health/Sexual Health",
    ]

    is_safe = True
    for category, confidence in categories.items():
        if any(uc in category for uc in unsafe_categories) and confidence > 0.5:
            is_safe = False
            break

    return SafetyResult(is_safe=is_safe, categories=categories)
