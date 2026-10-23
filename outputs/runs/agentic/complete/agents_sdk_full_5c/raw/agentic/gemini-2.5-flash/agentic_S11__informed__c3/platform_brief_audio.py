import os
from google.cloud import texttospeech

def generate_audio_google_cloud_tts(text: str, output_filepath: str, voice_name: str = "en-US-Standard-C", audio_format: str = "MP3") -> dict:
    """
    Generates spoken briefings from platform outputs using Google Cloud Text-to-Speech.
    Requires GOOGLE_APPLICATION_CREDENTIALS to be set.
    """
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Select the voice parameters
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name=voice_name,
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL, # Can be MALE, FEMALE, NEUTRAL
    )

    # Select the type of audio file you want returned
    audio_encoding_map = {
        "MP3": texttospeech.AudioEncoding.MP3,
        "LINEAR16": texttospeech.AudioEncoding.LINEAR16, # WAV
        "OGG_OPUS": texttospeech.AudioEncoding.OGG_OPUS,
    }
    audio_config = texttospeech.AudioConfig(
        audio_encoding=audio_encoding_map.get(audio_format.upper(), texttospeech.AudioEncoding.MP3)
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # The response's audio_content is binary. Save it to a file.
    with open(output_filepath, "wb") as out:
        out.write(response.audio_content)
        print(f'Audio content written to file "{output_filepath}"')
    
    return {
        "output_filepath": output_filepath,
        "audio_content_length": len(response.audio_content),
        "raw_response": response # Preserve the original response object
    }

if __name__ == '__main__':
    # Example usage
    # Ensure GOOGLE_APPLICATION_CREDENTIALS is set.
    sample_text = "This is a brief audio summary generated from the platform output."
    output_file = "briefing.mp3"

    try:
        audio_results = generate_audio_google_cloud_tts(sample_text, output_file)
        print(f"Audio briefing successfully generated at {audio_results['output_filepath']}")
    except Exception as e:
        print(f"An error occurred during audio generation: {e}")
