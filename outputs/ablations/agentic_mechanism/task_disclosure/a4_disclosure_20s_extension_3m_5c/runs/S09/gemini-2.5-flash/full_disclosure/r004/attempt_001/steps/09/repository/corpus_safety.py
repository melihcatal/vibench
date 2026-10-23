from google.cloud import language_v1

def check_corpus_safety(text: str) -> dict:
    """
    Checks the safety of the corpus text before embedding using Google Cloud Natural Language API.

    Args:
        text: The text string to be checked for safety.

    Returns:
        A dictionary containing the safety check results.
    """
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)

    # Perform content moderation (e.g., sentiment analysis as a proxy for safety in this example)
    # For actual content safety, you might use other APIs or specific models.
    # This example uses sentiment analysis to demonstrate interaction with the NL API.
    response = client.analyze_sentiment(document=document)
    
    # You would typically analyze the categories and their scores for actual safety checks.
    # For a direct safety API, you would use a dedicated content moderation service if available.
    
    return {
        "score": response.document_sentiment.score,
        "magnitude": response.document_sentiment.magnitude,
        "language": response.language
    }
