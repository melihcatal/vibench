import asyncio
import os
from google.cloud import language

language_client = language.LanguageServiceClient()

async def caption_embedding(text):
    document = language.Document(content=text, type_=language.Document.Type.PLAIN_TEXT)
    embedding = language_client.analyze_sentiment(document=document).document_sentiment.score
    return embedding