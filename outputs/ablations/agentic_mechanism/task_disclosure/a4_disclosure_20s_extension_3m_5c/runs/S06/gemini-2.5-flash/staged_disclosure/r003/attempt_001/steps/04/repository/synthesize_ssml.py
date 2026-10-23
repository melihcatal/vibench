
from google.cloud import texttospeech

def synthesize_ssml(ssml_text, output_filename="output.mp3"):
    """Synthesizes SSML with voice and prosody controls using Google Cloud Text-to-Speech."""

    client = texttospeech.TextToSpeechClient()

    input_text = texttospeech.SynthesisInput(ssml=ssml_text)

    # Select the voice and prosody controls
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name="en-US-Wavenet-D",  # Example: a Wavenet voice
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL,
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
    # Example SSML with prosody controls
    ssml_example = """
    <speak>
      <prosody rate="slow" pitch="-2st">
        This is an example of speech with a slower rate and a lower pitch.
      </prosody>
      <break time="1s"/>
      <prosody volume="+6dB">
        And this part is spoken with increased volume!
      </prosody>
    </speak>
    """
    synthesize_ssml(ssml_example, "ssml_prosody_example.mp3")
