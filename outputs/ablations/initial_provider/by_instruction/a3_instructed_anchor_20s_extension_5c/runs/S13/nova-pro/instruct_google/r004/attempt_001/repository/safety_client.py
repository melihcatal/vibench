import os
from google.cloud import language_v1

def get_language_client():
    return language_v1.LanguageServiceClient()

def get_document(text):
    return language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
