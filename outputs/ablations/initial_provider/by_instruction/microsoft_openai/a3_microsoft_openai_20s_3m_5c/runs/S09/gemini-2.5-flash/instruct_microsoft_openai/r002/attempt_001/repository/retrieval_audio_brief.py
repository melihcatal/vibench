import os
from typing import List
from google.cloud import texttospeech

# Note: Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set for Google Cloud authentication

def generate_audio_brief(text: str, output_filename: str = "audio_brief.mp3") -> str:
    client = texttospeech.TextToSpeechClient()
    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Select the language and SSML voice type
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Perform the text-to-speech request on the text input with the selected voice parameters and audio file type
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # The response's audio_content is binary. Write it to a file.
    with open(output_filename, "wb") as out:
        out.write(response.audio_content)

    return output_filename

def retrieval_audio_brief(retrieved_results: List[str], brief_title: str = "Search Results Brief") -> str:
    brief_text = f"Hello! Here is a brief summary of your search results for {brief_title}.\n\n"
    for i, result in enumerate(retrieved_results):
        brief_text += f"Result {i+1}: {result}\n\n"
    
    output_file = f"retrieval_brief_{brief_title.replace(' ', '_').lower()}.mp3"
    return generate_audio_brief(brief_text, output_file)
