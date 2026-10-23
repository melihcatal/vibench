from google.cloud import texttospeech

def synthesize_ssml(ssml_text, output_filename):
    """Synthesizes SSML with voice and prosody controls."""
    client = texttospeech.TextToSpeechClient()

    input_text = texttospeech.SynthesisInput(ssml=ssml_text)

    # Select the voice and audio file type
    # You can find a list of supported voices and languages here:
    # https://cloud.google.com/text-to-speech/docs/voices
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name="en-US-Wavenet-D",  # Example: a Wavenet voice
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL,
    )

    # Select the type of audio file you want to return
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Perform the text-to-speech request
    response = client.synthesize_speech(
        input=input_text, voice=voice, audio_config=audio_config
    )

    # Write the response audio content to the output file.
    with open(output_filename, "wb") as out:
        out.write(response.audio_content)
        print(f'Audio content written to file "{output_filename}"')

if __name__ == "__main__":
    # Example SSML text with prosody controls
    # You can adjust rate, pitch, and volume as needed.
    # See more SSML tags here: https://cloud.google.com/text-to-speech/docs/ssml
    example_ssml = """
    <speak>
      <prosody rate="slow" pitch="+2st">
        Hello there! This is an example of SSML synthesis.
      </prosody>
      <break time="1s"/>
      <prosody volume="+6dB">
        I can speak louder and with a different pace.
      </prosody>
    </speak>
    """
    synthesize_ssml(example_ssml, "output_ssml.mp3")
