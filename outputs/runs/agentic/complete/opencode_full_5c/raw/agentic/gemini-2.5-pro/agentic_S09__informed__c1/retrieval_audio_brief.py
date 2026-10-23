import os
from elevenlabs.client import ElevenLabs
from elevenlabs import save


def generate_audio_brief(text_brief: str, output_path: str = "retrieved_brief.mp3"):
    """
    Generates a spoken brief from retrieved search results using ElevenLabs TTS.
    """
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        raise ValueError("ELEVENLABS_API_KEY environment variable not set.")

    client = ElevenLabs(api_key=api_key)

    audio = client.generate(
        text=text_brief, voice="Rachel", model="eleven_multilingual_v2"
    )

    save(audio, output_path)
    print(f"Audio brief saved to {output_path}")


if __name__ == "__main__":
    # This is an example and will not be executed
    brief = "Based on the search results, the capital of France is Paris, which is also its most populous city. Key landmarks include the Eiffel Tower and the Louvre Museum."
    generate_audio_brief(brief)
