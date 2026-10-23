from google.cloud import language_v1

def check_message_safety(message_text: str) -> Dict[str, Any]:
    """Checks message payload text for unsafe content using Google Cloud Natural Language API.

    Args:
        message_text: The text content of the message payload.

    Returns:
        A dictionary containing safety analysis results (e.g., categories indicating unsafe content).
    """
    client = language_v1.LanguageServiceClient()

    document = language_v1.Document(
        content=message_text, type=language_v1.Document.Type.PLAIN_TEXT
    )

    # Classify text to find categories that might indicate unsafe content
    # Note: This is a basic example. Real-world content moderation might require a more sophisticated approach
    # or a dedicated content moderation API.
    response = client.classify_text(request={'document': document})

    unsafe_categories = [
        "/Law & Government/Legal Issues/Crime & Justice",
        "/Sensitive Subjects/Discrimination",
        "/Sensitive Subjects/Illegal Activities",
        "/Sensitive Subjects/Offensive Content",
        "/Sensitive Subjects/Violence",
    ]

    safety_results = {"is_safe": True, "unsafe_flags": []}
    for category in response.categories:
        if category.name in unsafe_categories:
            safety_results["is_safe"] = False
            safety_results["unsafe_flags"].append(
                {"category": category.name, "confidence": category.confidence}
            )
    return safety_results
