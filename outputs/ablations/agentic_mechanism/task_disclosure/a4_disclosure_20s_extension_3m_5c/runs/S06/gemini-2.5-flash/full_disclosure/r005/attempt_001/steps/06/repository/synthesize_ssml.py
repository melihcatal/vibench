import os
from google.cloud import texttospeech

def synthesize_ssml(ssml_content: str, voice_name: str, language_code: str = "en-US") -> bytes:
    """
    Synthesizes SSML content with voice and prosody controls using Google Cloud Text-to-Speech.

    Args:
        ssml_content: The SSML input to be synthesized.
        voice_name: The name of the voice to use (e.g., "en-US-Wavenet-D").
        language_code: The language code for the voice (e.g., "en-US").

    Returns:
        The audio content as bytes.
    """
    # Instantiates a client
    client = texttospeech.TextToSpeechClient()  # Google Cloud Text-to-Speech client

    # Set the SSML input
    synthesis_input = texttospeech.SynthesisInput(ssml=ssml_content)

    # Select the voice
    voice = texttospeech.VoiceSelectionParams(
        language_code=language_code,
        name=voice_name
    )

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Perform the text-to-speech request on the SSML input with the selected voice parameters and audio file type
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    return response.audio_content

if __name__ == "__main__":
    # Example usage:
    # Set your GOOGLE_APPLICATION_CREDENTIALS environment variable
    # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/your/key.json"

    sample_ssml = """
    <speak>
      Hello, this is a sample text with <prosody rate="slow">slow speech</prosody> and
      <emphasis level="strong">strong emphasis</emphasis>.
      <break time="1s"/>
      And here is a pause.
    </speak>
    """
    selected_voice = "en-US-Wavenet-D" # Example Wavenet voice

    try:
        audio_bytes = synthesize_ssml(sample_ssml, selected_voice)
        with open("output_ssml.mp3", "wb") as out:
            out.write(audio_bytes)
        print("Audio content written to file output_ssml.mp3")
    except Exception as e:
        print(f"An error occurred: {e}")
        print("Please ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set correctly and the voice name is valid.")
