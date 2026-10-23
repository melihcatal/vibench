from google.cloud import texttospeech
import os

def synthesize_ssml_text(ssml: str, output_filepath: str, voice_name: str = "en-US-Wavenet-D", language_code: str = "en-US"):
    """
    Synthesizes SSML with voice and prosody controls using Google Cloud Text-to-Speech.
    """
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(ssml=ssml)

    voice = texttospeech.VoiceSelectionParams(
        language_code=language_code,
        name=voice_name
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    with open(output_filepath, "wb") as out:
        out.write(response.audio_content)
    print(f"Audio content written to file '{output_filepath}'")

if __name__ == "__main__":
    # Example usage (ensure GOOGLE_APPLICATION_CREDENTIALS is set)
    # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/your/key.json"
    ssml_text = """
    <speak>
      <prosody rate="slow">This is an example of SSML synthesis.</prosody>
      <emphasis level="strong">It allows for more control</emphasis> over the spoken output.
    </speak>
    """
    synthesize_ssml_text(ssml_text, "output_ssml.mp3")
