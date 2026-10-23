from google.cloud import texttospeech

def synthesize_ssml(text, output_filename):
    """Synthesizes SSML with voice and prosody controls."""
    client = texttospeech.TextToSpeechClient()

    # Set the SSML input with voice and prosody controls
    ssml_text = f"""<speak>
        <prosody rate="slow" pitch="+2st">
            Hello, <emphasis level="strong">world</emphasis>!
        </prosody>
        <break time="1s"/>
        I can also speak with a <prosody volume="loud">louder volume</prosody>.
    </speak>"""

    synthesis_input = texttospeech.SynthesisInput(ssml=ssml_text)

    # Select the voice parameters.
    # A list of available voices can be found at
    # https://cloud.google.com/text-to-speech/docs/voices
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name="en-US-Wavenet-D",  # Example: a neural2 voice
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL,
    )

    # Select the type of audio file you want returned.
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Perform the text-to-speech request
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # Write the response to the output file.
    with open(output_filename, "wb") as out:
        out.write(response.audio_content)
        print(f'''Audio content written to file "{output_filename}"''')

if __name__ == "__main__":
    synthesize_ssml("example_ssml.mp3")
