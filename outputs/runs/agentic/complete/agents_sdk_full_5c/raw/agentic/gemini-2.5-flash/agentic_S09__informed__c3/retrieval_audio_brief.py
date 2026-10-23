import os
from google.cloud import texttospeech

def generate_audio_brief(text_brief: str, output_filename: str = "audio_brief.mp3"):
    """
    Generates a spoken audio brief from retrieved search results using Google Cloud Text-to-Speech.

    Args:
        text_brief: The text content of the brief to convert to speech.
        output_filename: The name of the file to save the audio to (e.g., "brief.mp3").
    """
    # Requires GOOGLE_APPLICATION_CREDENTIALS to be set in the environment
    # or configured via gcloud auth application-default login
    # Provider-identifying signal: google.cloud.texttospeech
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text_brief)

    # Configure the voice request
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL,
    )

    # Configure the audio file type
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # The response's audio_content is binary.
    with open(output_filename, "wb") as out:
        out.write(response.audio_content)
        print(f'Audio content written to file "{output_filename}"')

if __name__ == '__main__':
    brief_text = """
    Here is a brief summary of your search results. 
    The top result indicates that the new policy will be implemented next quarter. 
    There is also a related document detailing the impact on regional offices.
    For more information, please refer to the full report.
    """
    
    generate_audio_brief(brief_text, "search_brief.mp3")
    print("Generated 'search_brief.mp3' containing the audio brief.")
