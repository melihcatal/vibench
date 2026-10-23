from google.cloud import language_v2

def moderate_transcript(text_content: str):
    """Moderates the given text using Google Cloud Natural Language API."""
    client = language_v2.LanguageServiceClient()

    document = language_v2.Document(
        content=text_content, type_=language_v2.Document.Type.PLAIN_TEXT
    )

    # Use the moderate_text method
    response = client.moderate_text(document=document)

    # You can process the response further based on your moderation needs.
    # For example, print categories and their confidence scores.
    # Here, we'll return the full response.
    return response

