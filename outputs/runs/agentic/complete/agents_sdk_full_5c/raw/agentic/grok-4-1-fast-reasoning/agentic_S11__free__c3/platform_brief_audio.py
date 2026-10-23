import os
from elevenlabs import ElevenLabs
from elevenlabs.speech import SpeechSynthesisResponse

def platform_brief_audio(output: str) -> bytes:
    client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))
    audio = client.generate(
        text=output,
        voice="21m00Tcm4TlvDq8ikWAM",  # Rachel voice ID
        model="eleven_monolingual_v1"
    )
    return audio
