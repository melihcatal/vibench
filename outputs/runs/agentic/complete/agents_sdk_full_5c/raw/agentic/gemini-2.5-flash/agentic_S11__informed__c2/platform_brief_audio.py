from google.cloud import texttospeech
import os

def generate_spoken_briefing(text: str, output_file_path: str, voice_name: str = "en-US-Neural2-D") -> dict:
    """
    Generates spoken briefings from platform outputs using Google Cloud Text-to-Speech.
    
    Args:
        text: The text to convert to speech.
        output_file_path: The path where the generated audio file will be saved (e.g., "briefing.mp3").
        voice_name: The name of the voice to use (e.g., "en-US-Neural2-D", "en-GB-Wavenet-A").
        
    Returns:
        A dictionary containing the path to the audio file and its MIME type.
    """
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Select the language and SSML voice type
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name=voice_name,
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL,
    )

    # Select the type of audio file you want to return
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # The response's audio_content is binary.
    with open(output_file_path, "wb") as out:
        out.write(response.audio_content)
        # print(f'Audio content written to file "{output_file_path}"')
        
    return {
        "audio_file_path": output_file_path,
        "mime_type": "audio/mpeg"
    }

if __name__ == '__main__':
    # Example usage
    # Ensure GOOGLE_APPLICATION_CREDENTIALS is set or you are authenticated via gcloud
    # briefing_text = "Good morning. Here is a brief update on today's weather. Expect clear skies with a high of 75 degrees Fahrenheit."
    # output_path = "weather_briefing.mp3"

    # print(f"Generating audio briefing to {output_path}...")
    # try:
    #     audio_info = generate_spoken_briefing(briefing_text, output_path)
    #     print(f"Audio briefing created at: {audio_info['audio_file_path']}")
    #     print(f"MIME type: {audio_info['mime_type']}")
    # except Exception as e:
    #     print(f"Error generating audio briefing: {e}")
