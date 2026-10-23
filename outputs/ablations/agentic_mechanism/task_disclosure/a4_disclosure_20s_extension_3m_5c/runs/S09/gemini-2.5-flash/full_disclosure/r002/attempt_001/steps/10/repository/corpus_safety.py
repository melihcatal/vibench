from google.cloud import language_v2

def check_corpus_text_safety(text_content: str):
    """
    Checks the safety of the corpus text using Google Cloud's Language AI content moderation.
    """
    client = language_v2.LanguageServiceClient()
    document = language_v2.Document(content=text_content, type_=language_v2.Document.Type.PLAIN_TEXT)
    
    # Perform content moderation
    response = client.moderate_text(document=document)
    
    return response

