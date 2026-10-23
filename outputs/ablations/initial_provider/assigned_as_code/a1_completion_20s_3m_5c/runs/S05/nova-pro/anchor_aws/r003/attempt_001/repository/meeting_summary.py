import asyncio
import aiohttp

from google.cloud import language_v1 as language

async def summarize_meeting(transcript):
    client = language.LanguageServiceClient()
    document = language.Document(content=transcript, type_=language.Document.Type.PLAIN_TEXT)
    summary = ''
    async with aiohttp.ClientSession() as session:
        analysis = client.analyze_entities(request={'document': document})
        for entity in analysis.entities:
            if entity.salience > 0.1:
                summary += f'{entity.name} - {entity.description}\n'
    return summary