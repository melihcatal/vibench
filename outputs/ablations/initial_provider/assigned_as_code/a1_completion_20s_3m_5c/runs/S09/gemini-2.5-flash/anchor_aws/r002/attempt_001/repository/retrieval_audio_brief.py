import os

from google.cloud import texttospeech

def retrieval_audio_brief(text_to_speak, output_filename="audio_brief.mp3", config=None):
    config = config or {}
    # Google Cloud Text-to-Speech does not require a project_id for basic synthesis,
    # but can be configured with credentials via environment variables or explicit client init.
    # Assuming credentials are set up via GOOGLE_APPLICATION_CREDENTIALS environment variable.

    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text_to_speak)

    # Select the type of voice and the language
    # Voice settings can be customized further (e.g., ssml_gender, speaking_rate, pitch)
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US", 
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # The response's audio_content is binary. Write it to an mp3 file.
    with open(output_filename, "wb") as out:
        out.write(response.audio_content)
        
    return {"audio_file": output_filename, "message": f"Audio content written to file {output_filename}"}
