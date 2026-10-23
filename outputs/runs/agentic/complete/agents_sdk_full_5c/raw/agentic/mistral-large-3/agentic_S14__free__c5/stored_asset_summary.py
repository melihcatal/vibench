from google.cloud import language_v1


def summarize_text(text: str) -> str:
    """
    Summarize content extracted from a stored asset using Google Cloud Natural Language API.
    
    Args:
        text: Text to summarize.
        
    Returns:
        Summary of the text.
    """
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(
        content=text, type_=language_v1.Document.Type.PLAIN_TEXT
    )

    response = client.analyze_entities(
        request={"document": document}
    )

    entities = [entity.name for entity in response.entities]
    return " ".join(entities)