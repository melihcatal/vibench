import asyncio
import os
from typing import AsyncGenerator, AsyncIterable
import google.generativeai as genai
import google.generativeai.types as types

genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
model = genai.GenerativeModel(
    model_name='gemini-1.5-flash',
    generation_config=types.GenerationConfig(temperature=0.3)
)
chat = model.start_chat()

async def summarize_live_meeting_transcript(
    transcript_chunks: AsyncIterable[str]
) -> AsyncGenerator[str, None]:
    buffer = ''
    async for chunk in transcript_chunks:
        buffer += chunk + ' '
        if len(buffer) > 2000:
            prompt = f'Summarize this live meeting transcript chunk as key points:\\n{buffer}'
            response = await asyncio.to_thread(chat.send_message, prompt)
            yield response.text
            buffer = ''
    if buffer.strip():
        prompt = f'Summarize this live meeting transcript chunk as key points:\\n{buffer}'
        response = await asyncio.to_thread(chat.send_message, prompt)
        yield response.text
