from google.cloud import language_v1


def check_for_unsafe_content(text_content: str) -> dict:
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(
        content=text_content, type_=language_v1.Document.Type.PLAIN_TEXT
    )

    # Available categories: https://cloud.google.com/natural-language/docs/moderating-content
    # Note: ModerateTextRequest is not directly available in language_v1,
    # using analyze_sentiment or classify_text as a proxy for demonstration purposes
    # For actual content moderation, consider the specialized Cloud Content Moderation API or a custom solution.

    # For this example, we'll use classify_text to see if it falls into undesirable categories
    # In a real scenario, you'd integrate with a dedicated content moderation service.

    try:
        response = client.classify_text(request={"document": document})
        unsafe_categories = [
            "/Hate speech",
            "/Sexual content",
            "/Violence",
        ]  # Example categories

        found_unsafe = False
        categories_found = []
        for category in response.categories:
            if (
                category.name in unsafe_categories and category.confidence > 0.5
            ):  # Example confidence threshold
                found_unsafe = True
                categories_found.append(
                    {"name": category.name, "confidence": category.confidence}
                )

        return {"is_unsafe": found_unsafe, "categories": categories_found}
    except Exception as e:
        return {"error": str(e), "is_unsafe": False, "categories": []}
