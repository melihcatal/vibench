from embeddings_client import get_elevenlabs_client
from elevenlabs import save


def generate_audio_brief(text: str, output_path: str = "retrieval_brief.mp3"):
    """
    Generates a spoken brief from retrieved search results using ElevenLabs API.
    """
    client = get_elevenlabs_client()

    audio = client.generate(text=text, voice="Rachel", model="eleven_multilingual_v2")

    save(audio, output_path)
    return output_path
