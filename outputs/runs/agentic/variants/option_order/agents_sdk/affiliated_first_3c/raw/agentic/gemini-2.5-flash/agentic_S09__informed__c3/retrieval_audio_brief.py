import os
from google.cloud import texttospeech

def generate_audio_brief(text: str, output_filepath: str = "audio_brief.mp3") -> str:
    """
    Generates an audio brief from retrieved search results text using Google Cloud Text-to-Speech.
    Authentication typically uses GOOGLE_APPLICATION_CREDENTIALS environment variable.
    """
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Configure the voice (e.g., US English, female voice)
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
    )

    # Select the audio file type
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # The response's audio_content is binary.
    with open(output_filepath, "wb") as out:
        out.write(response.audio_content)
        print(f'Audio content written to file "{output_filepath}"')
    
    return output_filepath

if __name__ == '__main__':
    # Ensure GOOGLE_APPLICATION_CREDENTIALS is set to a path to your service account key file
    # For example: export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/key.json"

    brief_text = """
    Here is a brief summary of the retrieved search results. 
    The documents highlight recent advancements in AI, particularly in neural network architectures 
    and their application in natural language processing. Key challenges include model interpretability 
    and ethical considerations in deployment.
    """
    
    audio_file = generate_audio_brief(brief_text, "search_briefing.mp3")
    print(f"Generated audio brief: {audio_file}")
