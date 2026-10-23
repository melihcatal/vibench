import google.cloud.language_v2 as language_v2

def check_corpus_safety(text: str) -> language_v2.ModerateTextResponse:
    """
    Checks the safety of the input text using Google Cloud Natural Language API's moderateText method.

    Args:
        text: The text string to be checked for safety.

    Returns:
        A ModerateTextResponse object containing safety attributes.
    """
    client = language_v2.LanguageServiceClient()
    document = language_v2.Document(content=text, type_=language_v2.Document.Type.PLAIN_TEXT)
    response = client.moderate_text(document=document)
    return response
