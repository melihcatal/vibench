from google.cloud import texttospeech
from typing import Dict, Any

def platform_brief_audio(project_id: str, text: str, output_filepath: str = "output_briefing.mp3", language_code: str = "en-US", voice_name: str = "en-US-Standard-C") -> Dict[str, Any]:
    """Generates spoken briefings from platform outputs using Google Cloud Text-to-Speech API.

    Args:
        project_id: Your Google Cloud project ID.
        text: The text content for the audio briefing.
        output_filepath: The path to save the generated audio file (e.g., 'briefing.mp3').
        language_code: The BCP-47 language code for the voice (e.g., 'en-US').
        voice_name: The name of the voice to use (e.g., 'en-US-Standard-C').

    Returns:
        A dictionary containing information about the generated audio file.
    """
    client = texttospeech.TextToSpeechClient()

    # Set the text input to be synthesized
    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Build the voice request, select the language code ("en-US") and the voice gender ("neutral")
    voice = texttospeech.VoiceSelectionParams(
        language_code=language_code,
        name=voice_name, # Example: 'en-US-Wavenet-D' for a premium voice
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL, # Can be MALE, FEMALE, NEUTRAL
    )

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    print(f"Generating audio for text (length {len(text)}) using voice {voice_name}...")
    
    # Perform the text-to-speech request on the text input with the selected voice parameters and audio file type
    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config
    )

    # The response's audio_content is binary. Write it to a file.
    try:
        with open(output_filepath, "wb") as out:
            out.write(response.audio_content)
        print(f'Audio content written to file "{output_filepath}"')
        audio_info = {
            "output_filepath": output_filepath,
            "text_length": len(text),
            "language_code": language_code,
            "voice_name": voice_name,
            "provider": "Google Cloud Text-to-Speech API"
        }
        return audio_info
    except Exception as e:
        print(f"Error writing audio file: {e}")
        return {"error": str(e)}

if __name__ == '__main__':
    # Replace with your actual project_id
    project_id = "your-gcp-project-id"
    briefing_text = "This is a short audio briefing generated from a platform output. It contains important updates about the project status and upcoming milestones."

    print("\n--- Generating Audio Briefing ---")
    audio_result = platform_brief_audio(
        project_id=project_id, 
        text=briefing_text, 
        output_filepath="project_briefing.mp3",
        voice_name="en-US-Wavenet-C" # Using a Wavenet voice for higher quality
    )
    print(audio_result)

    # Example with a different language (if supported by the voice name)
    # print("\n--- Generating Spanish Audio Briefing ---")
    # spanish_briefing_text = "Este es un breve informe de audio generado a partir de una salida de la plataforma."
    # audio_result_es = platform_brief_audio(
    #     project_id=project_id, 
    #     text=spanish_briefing_text, 
    #     output_filepath="spanish_briefing.mp3",
    #     language_code="es-ES",
    #     voice_name="es-ES-Wavenet-B"
    # )
    # print(audio_result_es)
