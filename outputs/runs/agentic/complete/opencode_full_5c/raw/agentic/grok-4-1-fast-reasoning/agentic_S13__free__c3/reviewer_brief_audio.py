from elevenlabs.client import ElevenLabs
from elevenlabs import save
from safety_client import get_api_key


def reviewer_brief_audio(
    brief_text: str, voice: str = "Rachel", output_file: str = "reviewer_brief.mp3"
) -> str:
    client = ElevenLabs(api_key=get_api_key("elevenlabs"))
    audio = client.generate(text=brief_text, voice=voice, model="eleven_monolingual_v1")
    save(audio, output_file)
    return output_file
