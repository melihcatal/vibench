from google.cloud import texttospeech
from model_models import LLM_Output
import os

# Google Cloud Text-to-Speech provider-identifying signal: google.cloud.texttospeech import, texttospeech.TextToSpeechClient

def generate_spoken_brief(text: str, output_filepath: str, project_id: str, language_code: str = "en-US", voice_name: str = "en-US-Standard-A") -> LLM_Output:
    """
    Generates a spoken brief from model output using Google Cloud Text-to-Speech.
    The output is saved as an audio file.
    """
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Select the voice parameters
    voice = texttospeech.VoiceSelectionParams(
        language_code=language_code,
        name=voice_name,
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )

    # Select the type of audio file you want to return
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
    
    return {"audio_filepath": output_filepath, "status": "success"}

if __name__ == '__main__':
    # Example usage (replace with your actual project ID)
    sample_model_output = "The quarterly report indicates a strong growth in the technology sector, driven by increased adoption of cloud services and artificial intelligence solutions. Investors are advised to monitor emerging market trends closely."
    output_audio_file = "brief.mp3"
    
    # Replace 'your-gcp-project-id' with your actual Google Cloud Project ID
    # For demonstration, using a placeholder. The project_id isn't strictly needed
    # for Text-to-Speech if authentication is handled via environment variables
    # or service account, but kept for consistency as per prompt guidelines.
    tts_result = generate_spoken_brief(sample_model_output, output_audio_file, project_id="your-gcp-project-id")
    print(f"Spoken brief generation result: {tts_result}")
    
    # To play the audio, you would need an audio player, e.g.,
    # import subprocess
    # subprocess.call(["mpg123", output_audio_file]) # Requires mpg123 to be installed
