import os
from google.cloud import texttospeech

# Assuming `model_models` is available in the local environment
from model_models import AudioBriefing

def generate_audio_briefing(text: str, language_code: str = "en-US", voice_name: str = "en-US-Standard-C", audio_format: texttospeech.SsmlVoiceGender = texttospeech.SsmlVoiceGender.NEUTRAL) -> AudioBriefing:
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text)

    voice = texttospeech.VoiceSelectionParams(
        language_code=language_code,
        name=voice_name,
        ssml_gender=audio_format,
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # The response.audio_content is the binary audio data
    audio_content = response.audio_content

    return AudioBriefing(
        audio_content=audio_content,
        format="mp3",
        raw_response=response # The full proto response object
    )

if __name__ == "__main__":
    # Ensure GOOGLE_APPLICATION_CREDENTIALS is set up for your environment
    # A Google Cloud Project ID is not strictly needed for client init, but for billing/project association.
    # It's good practice to ensure the project has the Text-to-Speech API enabled.

    text_to_speak = "This is an important briefing about the current status of the project. All systems are online and operational."
    output_filename = "briefing.mp3"

    try:
        print(f"\nGenerating audio for: '{text_to_speak}'")
        audio_briefing = generate_audio_briefing(text_to_speak)
        
        with open(output_filename, "wb") as out:
            out.write(audio_briefing.audio_content)
            print(f"Audio content written to '{output_filename}'")
        
        print(f"Audio format: {audio_briefing.format}")

    except Exception as e:
        print(f"An error occurred during audio generation: {e}")
        print("Please ensure Google Cloud Text-to-Speech API is enabled and authentication is correctly configured.")
