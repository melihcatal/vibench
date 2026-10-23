from google.cloud import language_v1 as language

def summarize_text(text):
    """Summarizes content extracted from a stored asset."""
    client = language.LanguageServiceClient()
    document = language.Document(content=text, type_=language.Document.Type.PLAIN_TEXT)
    summary = client.summarize(document=document).summary
    return summary