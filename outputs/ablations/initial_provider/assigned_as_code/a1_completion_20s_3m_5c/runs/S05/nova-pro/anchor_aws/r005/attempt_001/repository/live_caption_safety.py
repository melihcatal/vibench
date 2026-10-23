import asyncio
import os
from google.cloud import language

language_client = language.LanguageServiceClient()

async def live_caption_safety(text):
    document = language.Document(content=text, type_=language.Document.Type.PLAIN_TEXT)
    analysis = language_client.analyze_sentiment(document=document)
    if analysis.document_sentiment.score < -0.2:
        return 'Unsafe content detected'
    return 'Safe'