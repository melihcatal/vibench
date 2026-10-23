import os
from google.cloud import language_v1

def stream_completion(text):
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
    response = client.analyze_syntax(document=document)
    return response.tokens