from google.cloud import texttospeech_v1
import os

def generate_reviewer_brief_audio(text: str, output_audio_path: str, language_code: str = "en-US", voice_name: str = "en-US-Standard-W") -> str:
    """
    Generates spoken briefs for moderation reviewers using Google Cloud Text-to-Speech API.

    Args:
        text: The text of the brief to convert to audio.
        output_audio_path: The file path to save the generated audio (e.g., "brief.mp3").
        language_code: The BCP-47 language code for the voice.
        voice_name: The name of the voice to use (e.g., "en-US-Standard-W").

    Returns:
        The path to the generated audio file, or an error message.
    """
    client = texttospeech_v1.TextToSpeechClient()

    synthesis_input = texttospeech_v1.SynthesisInput(text=text)

    # Select the language code and the voice name
    voice = texttospeech_v1.VoiceSelectionParams(
        language_code=language_code,
        name=voice_name,
        ssml_gender=texttospeech_v1.SsmlVoiceGender.NEUTRAL,
    )

    # Select the type of audio file you want returned
    audio_config = texttospeech_v1.AudioConfig(
        audio_encoding=texttospeech_v1.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        request={"input": synthesis_input, "voice": voice, "audio_config": audio_config}
    )

    # The response's audio_content is binary.
    with open(output_audio_path, "wb") as out:
        out.write(response.audio_content)
        print(f'Audio content written to file "{output_audio_path}"')
    
    return output_audio_path

if __name__ == '__main__':
    # Ensure Google Cloud authentication is set up (e.g., GOOGLE_APPLICATION_CREDENTIALS)
    # This script assumes default credentials will be found.

    brief_text = "This is a brief for the moderation reviewer. The current case involves a severe hate speech violation. Please prioritize this case. The user has appealed the decision, claiming misunderstanding of context."
    output_file = "reviewer_brief.mp3"

    try:
        generated_file = generate_reviewer_brief_audio(brief_text, output_file)
        print(f"Successfully generated audio brief: {generated_file}")
        print("You can play this file to listen to the brief.")
    except Exception as e:
        print(f"Error generating audio brief: {e}")

    brief_text_es = "Este es un resumen para el revisor de moderación. El caso actual implica una violación grave de discurso de odio. Por favor, priorice este caso."
    output_file_es = "reviewer_brief_es.mp3"
    try:
        generated_file_es = generate_reviewer_brief_audio(brief_text_es, output_file_es, language_code="es-ES", voice_name="es-ES-Standard-A")
        print(f"Successfully generated Spanish audio brief: {generated_file_es}")
    except Exception as e:
        print(f"Error generating Spanish audio brief: {e}")
