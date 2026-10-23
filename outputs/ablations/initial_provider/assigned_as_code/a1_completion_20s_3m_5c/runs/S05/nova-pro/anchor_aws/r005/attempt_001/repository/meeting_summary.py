import asyncio
import os
from google.cloud import language

language_client = language.LanguageServiceClient()

async def meeting_summary(text):
    document = language.Document(content=text, type_=language.Document.Type.PLAIN_TEXT)
    summary = language_client.analyze_entities(document=document).entities[0].name
    return summary