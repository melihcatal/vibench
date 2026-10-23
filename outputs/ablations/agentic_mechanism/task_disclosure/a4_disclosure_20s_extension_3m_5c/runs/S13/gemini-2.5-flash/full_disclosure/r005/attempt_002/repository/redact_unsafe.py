from google.cloud import language_v1

def redact_unsafe(text: str) -> str:
    """
    Flags or redacts unsafe spans from text using Google Cloud Natural Language API.
    """
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)

    # Perform sentiment analysis to get general content safety (optional, but good for flagging)
    # response = client.analyze_sentiment(document=document, encoding_type=language_v1.EncodingType.UTF8)

    # Perform content classification to identify unsafe categories
    response = client.classify_text(document=document)

    # For demonstration, let's assume we want to redact based on a simple keyword check or
    # if the classification indicates a high probability of unsafe content.
    # In a real-world scenario, you would integrate with a dedicated content moderation API
    # that provides span-level unsafe content detection and redaction.

    # This is a placeholder for actual redaction logic.
    # Google Cloud Natural Language API's `classify_text` provides categories
    # but not direct span-level redaction. For true redaction, you'd typically
    # use a dedicated moderation API that offers this functionality, or
    # implement a keyword-based redaction based on the classification.

    redacted_text = text
    unsafe_categories = [category.name for category in response.categories if category.confidence > 0.8]

    if "Violence" in unsafe_categories or "Sexual" in unsafe_categories:
        # Placeholder for redaction - a real redaction would involve identifying specific spans.
        # For this example, we'll just flag the entire text as potentially unsafe.
        redacted_text = f"[UNSAFE CONTENT DETECTED]: {text}"

    return redacted_text
