import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def check_live_caption_safety(caption_stream):
    """Check live transcript text for unsafe content using OpenAI Moderation."""
    for caption in caption_stream:
        if caption.strip():
            response = client.moderations.create(
                model="moderation-latest",
                input=caption.strip()
            )
            result = response.results[0]
            if not result.flagged:
                yield caption
