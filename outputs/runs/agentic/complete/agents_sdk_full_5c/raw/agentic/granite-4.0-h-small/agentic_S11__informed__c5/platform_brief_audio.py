# platform_brief_audio.py
# Managed Model Platform Workflow: generate spoken briefings from model output
# Provider: ElevenLabs Text-to-Speech
import elevenlabs

# Load API key from environment variable
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")

elevenlabs.api_key = ELEVENLABS_API_KEY

def generate_speech(text: str, voice: str = "305") -> bytes:
    """Synthesize speech from text using ElevenLabs.

    Returns raw audio bytes in MP3 format.
    """
    response = elevenlabs.Speech.synthesize(text=text, voice=voice)
    # The SDK returns the audio as bytes directly
    return response.audio_content

if __name__ == "__main__":
    # Example briefing synthesis
    briefing = "Welcome to the daily news briefing. Today we discuss advancements in AI."
    audio_bytes = generate_speech(briefing)
    # For demonstration, write to a temporary file (not required by spec)
    import tempfile
    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tf:
        tf.write(audio_bytes)
        print(f"Audio written to {tf.name}")
