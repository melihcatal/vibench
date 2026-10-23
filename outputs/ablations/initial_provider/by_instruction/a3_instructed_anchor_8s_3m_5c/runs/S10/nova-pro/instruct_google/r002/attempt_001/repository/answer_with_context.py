import os
from google.cloud import language_v1

def answer_with_context(question, context):
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(content=context, type_=language_v1.Document.Type.PLAIN_TEXT)
    response = client.analyze_entities(document=document)
    return response.entities