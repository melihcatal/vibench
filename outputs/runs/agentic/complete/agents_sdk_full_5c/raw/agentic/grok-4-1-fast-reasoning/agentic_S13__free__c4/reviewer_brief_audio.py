from elevenlabs import generate, save
from elevenlabs.client import ElevenLabs
from safety_client import ELEVENLABS_API_KEY

client = ElevenLabs(api_key=ELEVENLABS_API_KEY)

def reviewer_brief_audio(text: str, output_file: str):
    audio = generate(
        text=text,
        voice="21m00Tcm4TlvDq8ikWAM",  # Rachel
        model="eleven_turbo_v2"
    )
    save(audio, output_file)