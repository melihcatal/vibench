import os
from google.cloud import texttospeech

def generate_spoken_brief(text_to_speak: str, output_filepath: str = "audio_brief.mp3") -> str:
    """
    Generates an audio file from text using Google Cloud Text-to-Speech.
    Requires GOOGLE_APPLICATION_CREDENTIALS to be set or configured for authentication.
    """
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text_to_speak)

    # Select the type of voice and the language
    # For a list of available voices, see: https://cloud.google.com/text-to-speech/docs/voices
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        request={
            "input": synthesis_input,
            "voice": voice,
            "audio_config": audio_config
        }
    )

    # The response's audio_content is binary. Write it to a file.
    with open(output_filepath, "wb") as out:
        out.write(response.audio_content)
    return f"Audio content written to file {output_filepath}"

if __name__ == '__main__':
    # Example usage (requires GOOGLE_APPLICATION_CREDENTIALS to be set, e.g., via a service account key file)
    # To run:
    # export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/keyfile.json"
    # python retrieval_audio_brief.py
    
    retrieved_summary = (
        "According to recent search results, the main points are: "
        "Artificial intelligence is rapidly advancing, with breakthroughs in large language models. "
        "These models are impacting natural language processing and various industries. "
        "Further research indicates a growing interest in ethical AI development."
    )
    audio_output_file = "retrieval_brief.mp3"

    try:
        print(f"Generating audio brief for: \"{retrieved_summary[:100]}...\"")
        result_message = generate_spoken_brief(retrieved_summary, audio_output_file)
        print(result_message)
        print(f"You can play the generated audio file: {audio_output_file}")
    except Exception as e:
        print(f"An error occurred during audio brief generation: {e}")
