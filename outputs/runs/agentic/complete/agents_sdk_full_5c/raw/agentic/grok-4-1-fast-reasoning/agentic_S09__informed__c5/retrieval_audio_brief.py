import os
from elevenlabs.client import ElevenLabs

def retrieval_audio_brief(retrieved_texts: list[str]) -&gt; bytes:
    brief_text = "Retrieved documents: " + "; ".join(retrieved_texts[:5])
    client = ElevenLabs(api_key=os.getenv('ELEVENLABS_API_KEY'))
    audio = client.generate(
        text=brief_text,
        voice="21m00Tcm4TlvDq8ikWAM",
        model="eleven_monolingual_v1"
    )
    return audio