import os
from anthropic import Anthropic

def summarize_live_meeting(transcript_chunk_generator):
    api_key = os.getenv('ANTHROPIC_API_KEY')
    if not api_key:
        raise ValueError('ANTHROPIC_API_KEY environment variable is required.')
    client = Anthropic(api_key=api_key)
    accumulated = ''
    chunk_count = 0
    for chunk in transcript_chunk_generator:
        accumulated += ' ' + chunk
        chunk_count += 1
        if chunk_count % 20 == 0 or chunk.endswith('.'):  # Summarize periodically
            message = client.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=300,
                temperature=0.7,
                system="You are a helpful meeting assistant. Provide concise summaries of the ongoing meeting.",
                messages=[{"role": "user", "content": f"Summarize this meeting transcript chunk: {accumulated}"}]
            )
            summary = message.content[0].text
            yield summary
            accumulated = summary  # Chain summaries
    if accumulated:
        message = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=300,
            temperature=0.7,
            messages=[{"role": "user", "content": f"Final summary: {accumulated}"}]
        )
        yield message.content[0].text