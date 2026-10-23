import os
from google.cloud import language_v1

def summarize_text(text):
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
    response = client.summarize(document=document)
    return response.summaries[0].content