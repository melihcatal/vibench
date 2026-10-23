import asyncio
import json
import speech_client as sc
import speech_models as sm
from dotenv import load_dotenv

load_dotenv()

# LLM provider configuration (Anthropic Claude example)
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')
if not ANTHROPIC_API_KEY:
    raise RuntimeError('Set ANTHROPIC_API_KEY environment variable')

from anthropic import Anthropic, HuggingFaceInstructEmbeddings, Client
client = Anthropic(api_key=ANTHROPIC_API_KEY)

async def summarize_transcript(transcript_chunks):
    """Combine chunks and send to LLM for summarization."""
    full_text = '\n'.join(chunk for chunk in transcript_chunks if chunk)
    # Prompt for summarization
    prompt = f'Summarize the following meeting transcript in 3 bullet points:\n\n{full_text}'
    response = await client.completions.create(
        model='claude-3-5-sonnet-20240620',
        max_tokens=500,
        temperature=0,
        system='You are an expert meeting summarizer.',
        messages=[{'role':'user','content':[{'type':'text','text':prompt}]}]
    )
    return response.completion.strip()

async def meeting_summary(audio_source):
    """Transcribe live audio and produce a meeting summary per chunk batch."""
    transcript_batches = []
    async for result in sc.stream_chunks(audio_source):
        if not result.get('final'):
            continue
        transcript = result.get('transcript', '')
        if transcript.strip():
            transcript_batches.append(transcript)
        # When a batch reaches a reasonable size, summarize
        if len(transcript_batches) >= 5:
            summary = await summarize_transcript(transcript_batches)
            print('=== Meeting Summary ===\n', summary, '\n=== End Summary ===\n')
            transcript_batches = []  # reset for next batch
    # Summarize any remaining chunks
    if transcript_batches:
        summary = await summarize_transcript(transcript_batches)
        print('Final Summary:', summary)
    return

if __name__ == '__main__':
    # Example usage with a file audio source
    import aiofiles
    async def file_audio_source(path):
        async with aiofiles.open(path, 'rb') as f:
            while chunk := await f.read(1024):
                yield chunk
                await asyncio.sleep(0.01)
    asyncio.run(meeting_summary(file_audio_source('meeting.wav')))
