import os
from google.cloud import language_v1

def create_request(text):
    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
    return document