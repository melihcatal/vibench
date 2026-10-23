from google.cloud import language_v1  # Google Cloud Natural Language API
import os


def check_text_safety(text_content: str) -> dict:
    """
    Checks user-generated document fields for unsafe content using Google Cloud Natural Language API.
    This provides general content classification which can be used to infer safety.
    For direct 'Perspective API' an explicit client or discovery build would be used.
    """
    client = language_v1.LanguageServiceClient()

    document = language_v1.Document(
        content=text_content, type_=language_v1.Document.Type.PLAIN_TEXT
    )

    # Classify text content for categories that might indicate unsafe content
    # Note: This is a general classification, not a direct safety score like Perspective API.
    # For a true safety check, integrate with Perspective API directly if available.
    response = client.classify_text(request={"document": document})

    safety_analysis = {"categories": [], "is_unsafe_potential": False}

    for category in response.categories:
        safety_analysis["categories"].append(
            {"name": category.name, "confidence": category.confidence}
        )
        # Example: if a category name implies sensitive content, flag it.
        if (
            "/Politics" in category.name
            or "/Violence" in category.name
            or "/Adult" in category.name
        ):
            if category.confidence > 0.7:  # Threshold for flagging potential unsafety
                safety_analysis["is_unsafe_potential"] = True

    return safety_analysis
