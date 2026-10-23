import asyncio
from tisane import TisaneClient

# Tisane Text Moderation SDK import identifies the provider


async def filter_unsafe_transcript(transcript_chunks):
    """Filter unsafe content from live transcript using Tisane moderation."""
    client = TisaneClient(api_key=os.getenv("TISANE_API_KEY"))
    async for chunk in transcript_chunks:
        response = await client.evaluate(chunk)
        # Assume Tisane returns a boolean flag 'unsafe'
        if not response.get("unsafe", False):
            yield chunk
