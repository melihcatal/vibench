from google.cloud import language_v1

def summarize_audit_events(events: list[str]) -> str:
    """
    Summarizes federated-login audit events using Google Cloud Natural Language API.

    Args:
        events: A list of strings, where each string is an audit event.

    Returns:
        A single string containing the summary of the audit events.
    """
    if not events:
        return "No audit events to summarize."

    client = language_v1.LanguageServiceClient()
    
    # Combine all events into a single document for summarization
    text_content = "\n".join(events)

    document = language_v1.Document(
        content=text_content, type_=language_v1.Document.Type.PLAIN_TEXT
    )

    # Calling the analyze_entities method to get a summary. 
    # Note: The Natural Language API doesn't have a direct "summarization" endpoint. 
    # For a simple summary, we can extract key entities and their salience, 
    # or use a different approach like extractive summarization based on sentences 
    # with high salience scores. For this example, we'll aim to extract key information 
    # that could form a summary.
    # For a more advanced summarization, a different Google Cloud AI service like 
    # Vertex AI with a summarization model would be more appropriate.
    # However, for the purpose of demonstrating a concrete provider and identifiable code,
    # and given the constraints, we will use entity analysis as a proxy for identifying
    # key aspects of the events, which can be interpreted as a form of summarization
    # in this context.

    response = client.analyze_entities(
        request={"document": document, "encoding_type": language_v1.EncodingType.UTF8}
    )

    summary_parts = []
    for entity in response.entities:
        # Focusing on entities that are more likely to be relevant for an audit summary
        if entity.type in [
            language_v1.Entity.Type.PERSON,
            language_v1.Entity.Type.ORGANIZATION,
            language_v1.Entity.Type.EVENT,
            language_v1.Entity.Type.LOCATION,
            language_v1.Entity.Type.OTHER,
        ]:
            summary_parts.append(f"- {entity.name} (Type: {language_v1.Entity.Type(entity.type).name})")
            # Optionally add more details like salience or mentions if needed

    if summary_parts:
        return "Key entities identified in audit events:\n" + "\n".join(summary_parts)
    else:
        return "Could not identify key entities for summarization."

