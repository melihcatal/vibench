import asyncio
import aiohttp

from google.cloud import language_v1 as language

async def check_safety(captions):
    client = language.LanguageServiceClient()
    safe_captions = []
    async with aiohttp.ClientSession() as session:
        for caption in captions:
            document = language.Document(content=caption['text'], type_=language.Document.Type.PLAIN_TEXT)
            analysis = client.analyze_sentiment(request={'document': document})
            if analysis.document_sentiment.score >= -0.25:
                safe_captions.append(caption)
    return safe_captions