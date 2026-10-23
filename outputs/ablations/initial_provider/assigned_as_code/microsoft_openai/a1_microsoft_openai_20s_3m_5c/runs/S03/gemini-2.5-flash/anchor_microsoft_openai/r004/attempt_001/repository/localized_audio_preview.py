import os
from google.cloud import texttospeech

def generate_audio_preview(text: str, language_code: str, voice_name: str = None, output_file: str = "audio_preview.mp3", project_id: str = None) -> str:
    project_id = project_id or os.environ.get("GOOGLE_CLOUD_PROJECT")

    if not project_id:
        raise ValueError("Google Cloud project ID not provided or found in GOOGLE_CLOUD_PROJECT environment variable.")

    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Select the language and voice
    # You can find available voices here: https://cloud.google.com/text-to-speech/docs/voices
    voice = texttospeech.VoiceSelectionParams(
        language_code=language_code,
        name=voice_name if voice_name else None, # e.g., 'en-US-Standard-C'
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Perform the text-to-speech request
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # The response's audio_content is binary. Write it to an output file.
    with open(output_file, "wb") as out:
        out.write(response.audio_content)
    return output_file
