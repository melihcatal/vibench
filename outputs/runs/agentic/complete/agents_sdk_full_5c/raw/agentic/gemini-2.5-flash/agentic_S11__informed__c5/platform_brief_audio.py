import os
from elevenlabs import generate, play, set_api_key # ElevenLabs SDK
from elevenlabs.types import Voice, VoiceSettings

def generate_audio_briefing(text: str, voice_id: str = "21m00Tcm4TlvDq8ikWAM", model_id: str = "eleven_monolingual_v1"):
    api_key = os.environ.get("ELEVENLABS_API_KEY") # Provider-specific environment variable

    if not api_key:
        print("Please set the ELEVENLABS_API_KEY environment variable.")
        return None

    set_api_key(api_key) # Set the API key globally for ElevenLabs SDK

    try:
        audio = generate(
            text=text,
            voice=Voice(
                voice_id=voice_id, # Provider-specific voice ID (e.g., Rachel)
                settings=VoiceSettings(stability=0.71, similarity_boost=0.5, style=0.0, use_speaker_boost=True)
            ),
            model=model_id # Provider-specific model ID
        )
        
        # The 'audio' object is typically bytes (e.g., MP3 content)
        # You might want to save it to a file or stream it.
        # For demonstration, we'll return the bytes.
        
        # To play the audio, you would typically save it or use a playback library
        # For simplicity, if `play` is desired, ensure necessary audio libraries are installed.
        # play(audio) 

        return {
            "audio_content": audio,
            "format": "mp3", # ElevenLabs often returns MP3
            "text_processed": text
        }
    except Exception as e:
        print(f"Error generating audio with ElevenLabs: {e}")
        return None

if __name__ == '__main__':
    briefing_text = "Here is a brief audio summary of the latest news. The stock market closed higher today, and the weather forecast indicates sunshine for the weekend."
    
    # Default voice ID for Rachel in ElevenLabs
    default_voice_id = "21m00Tcm4TlvDq8ikWAM" 

    print(f"Generating audio briefing for: '{briefing_text[:50]}...' using ElevenLabs...")
    audio_briefing = generate_audio_briefing(briefing_text, default_voice_id)

    if audio_briefing:
        print(f"Audio briefing generated. Content size: {len(audio_briefing['audio_content'])} bytes")
        print(f"Format: {audio_briefing['format']}")
        
        # Example: Save the audio to a file
        output_filename = "briefing.mp3"
        with open(output_filename, "wb") as f:
            f.write(audio_briefing["audio_content"])
        print(f"Audio saved to {output_filename}")

        # You can optionally uncomment the line below to play the audio if `sounddevice`
        # or similar is installed and configured.
        # from elevenlabs import play
        # play(audio_briefing["audio_content"])
        # print("Playing audio briefing (if audio playback is configured)...")

    else:
        print("Failed to generate audio briefing.")
