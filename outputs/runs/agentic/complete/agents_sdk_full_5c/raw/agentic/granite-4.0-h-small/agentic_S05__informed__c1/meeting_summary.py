import asyncio
import json
import os
from ibm_watsonx_ai import WatsonxAiClient
from ibm_watsonx_ai.auth import IAMTokenManager

# IBM watsonx.ai Granite model for summarization (reference provider)
WATSONX_APIKEY = os.getenv('WATSONX_API_KEY')
WATSONX_PROJECT_ID = os.getenv('WATSONX_PROJECT_ID')
token_manager = IAMTokenManager(apikey=WATSONX_APIKEY)
client = WatsonxAiClient(token_manager=token_manager)
SUMM_MODEL = 'ibm/granite-13b-code-instruct'  # model identifier (family)

async def summarize_meeting_chunks(caption_chunks):
    """Collect caption chunks and request a summary from watsonx.ai Granite model."""
    transcript = ''
    async for chunk in caption_chunks:
        transcript += ' ' + chunk
    # Construct a prompt for summarization
    prompt = {
        'messages': [
            {'role': 'user', 'content': f'Summarize the following meeting transcript in 3 bullet points: {transcript}'},
        ]
    }
    result = client.completion(
        model=SUMM_MODEL,
        messages=prompt['messages'],
        max_tokens=100
    )
    summary = result.get('result', {}).get('choices', [{}])[0].get('message', {}).get('content', '')
    print('Meeting Summary:', summary)
    return summary

# Usage placeholder:
# async for chunk in async_caption_source():
#     await summarize_meeting_chunks([chunk])  # or accumulate first then call
