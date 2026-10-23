import os
from google.cloud import texttospeech_v1 as texttospeech

def generate_audio_brief(text: str, output_filepath: str = "brief.mp3"):
    """
    Generates an audio brief from retrieved search results text using Google Cloud Text-to-Speech.

    Args:
        text: The text content for the audio brief.
        output_filepath: The path to save the generated audio file (e.g., "brief.mp3").
    """
    client = texttospeech.TextToSpeechClient() # Google Cloud Text-to-Speech client

    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Configure the voice request
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL,
    )

    # Configure the audio format
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Perform the text-to-speech request
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # Write the response audio content to a file
    with open(output_filepath, "wb") as out:
        out.write(response.audio_content)
    print(f"Audio content written to file: {output_filepath}")

if __name__ == '__main__':
    sample_brief_text = """
    Here is a brief summary of your search results regarding artificial intelligence:
    Artificial intelligence is a broad field of computer science that gives computers the ability to imitate human intelligence.
    Key recent advancements include large language models and deep learning techniques.
    These technologies are rapidly transforming various industries and research areas.
    """
    generate_audio_brief(sample_brief_text, "ai_brief.mp3")
