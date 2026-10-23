import os
from elevenlabs.client import ElevenLabs
from elevenlabs import Voice, VoiceSettings, play

def generate_spoken_brief_elevenlabs(text: str, output_filepath: str = "brief.mp3", voice_id: str = "21m00Tcm4acsO3zW-x8Q") -> str:
    """
    Generates an audio brief from text using Eleven Labs Text-to-Speech and saves it to a file.
    Default voice is 'Rachel'.
    """
    client = ElevenLabs(api_key=os.environ.get("ELEVEN_API_KEY"))
    
    try:
        audio = client.generate(
            text=text,
            voice=Voice(
                voice_id=voice_id,
                settings=VoiceSettings(stability=0.75, similarity_boost=0.75, style=0.0, use_speaker_boost=True)
            ),
            model="eleven_multilingual_v2" # Or "eleven_monolingual_v1", etc.
        )

        with open(output_filepath, "wb") as f:
            for chunk in audio:
                if chunk:
                    f.write(chunk)
        return output_filepath
    except Exception as e:
        print(f"Error generating spoken brief with Eleven Labs: {e}")
        return "" # Indicate failure
