# Summarize live meeting transcript chunks
# Service: Gemini API (text chat / summarization)
# SDK: google-genai
# Authentication: GOOGLE_API_KEY

import os
import google.generativeai as genai
from typing import AsyncIterable, AsyncIterator

# Initialize Gemini model (adjust model name as needed)
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')  # or 'gemini-pro'

def _chunk(text: str, chunk_size: int = 400) -> AsyncIterable[str]:
    """Yield text chunks preserving sentence boundaries where possible.","""
    lines = text.splitlines()
    buffer = []
    for line in lines:
        buffer.append(line)
        if sum(len(l) for l in buffer) > chunk_size:
            yield \"\\n\".join(buffer)
            buffer = []
    if buffer:
        yield \"\\n\".join(buffer)

async def summarize_live_meeting(source: AsyncIterable[str]) -> AsyncIterable[str]:
    """Yield a short summary for each meeting transcript chunk.","""
    for chunk in _chunk(source):
        response = model.generate_content(chunk, generation_config=genai.GenerationConfig(
            temperature=0.0,
            max_output_tokens=150
        ))
        summary = response.text.strip()
        yield summary

# Example placeholder usage (needs full async driver)
# async for summary in summarize_live_meeting(transcript_stream()):
#     print("Summary:", summary)
