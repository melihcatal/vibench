from google.cloud import texttospeech

def synthesize_ssml(ssml_text: str, output_filename: str = "output.mp3"):
    """Synthesizes SSML with voice and prosody controls using Google Cloud Text-to-Speech.

    Args:
        ssml_text: The SSML text to synthesize.
        output_filename: The name of the output audio file.
    """
    client = texttospeech.TextToSpeechClient()

    input_text = texttospeech.SynthesisInput(ssml=ssml_text)

    # Select the language and SSML voice gender (e.g., "en-US", "FEMALE")
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        ssml_gender=texttospeech.SsmlVoiceGender.FEMALE,
    )

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=input_text, voice=voice, audio_config=audio_config
    )

    # The response's audio_content is binary.
    with open(output_filename, "wb") as out:
        out.write(response.audio_content)
        print(f'Audio content written to file "{output_filename}"')

if __name__ == "__main__":
    # Example SSML text with prosody controls
    example_ssml = """
    <speak>
      <prosody rate="slow" pitch="+2st">Hello there!</prosody>
      This is an example of <emphasis level="strong">SSML synthesis</emphasis>
      with Google Cloud Text-to-Speech.
      <break time="1s"/>
      <prosody volume="+6dB">I can speak louder now.</prosody>
    </speak>
    """
    synthesize_ssml(example_ssml, "ssml_output.mp3")
