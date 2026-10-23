import os
from google.cloud import texttospeech_v1

def generate_spoken_brief(text: str, output_filepath: str, language_code: str = "en-US", voice_name: str = "en-US-Standard-A") -> None:
    """
    Generates a spoken brief from text using Google Cloud Text-to-Speech.
    Saves the audio to the specified output_filepath.
    Requires GOOGLE_APPLICATION_CREDENTIALS environment variable.
    """
    client = texttospeech_v1.TextToSpeechClient()

    synthesis_input = texttospeech_v1.SynthesisInput(text=text)

    voice = texttospeech_v1.VoiceSelectionParams(
        language_code=language_code,
        name=voice_name,
        ssml_gender=texttospeech_v1.SsmlVoiceGender.NEUTRAL,
    )

    audio_config = texttospeech_v1.AudioConfig(
        audio_encoding=texttospeech_v1.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        request={
            "input": synthesis_input,
            "voice": voice,
            "audio_config": audio_config,
        }
    )

    with open(output_filepath, "wb") as out:
        out.write(response.audio_content)
    print(f'Audio content written to file "{output_filepath}"')

if __name__ == '__main__':
    # Example usage (requires GOOGLE_APPLICATION_CREDENTIALS env var)
    # generate_spoken_brief("Hello, this is a test spoken brief from Google Cloud Text-to-Speech.", "test_brief.mp3")
    pass
