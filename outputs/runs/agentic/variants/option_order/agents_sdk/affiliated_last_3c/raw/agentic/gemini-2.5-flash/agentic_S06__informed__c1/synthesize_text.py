from google.cloud import texttospeech
import os

def synthesize_text_to_audio(text: str, voice_name: str = "en-US-Wavenet-D") -> bytes:
    """Synthesizes plain text to an audio byte stream using Google Cloud Text-to-Speech.
    
    Args:
        text: The plain text to synthesize.
        voice_name: The desired voice name (e.g., "en-US-Wavenet-D").
        
    Returns:
        The audio content as bytes.
    """
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text)
    
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name=voice_name,
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )
    
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )
    
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )
    
    return response.audio_content

if __name__ == '__main__':
    # Ensure GOOGLE_APPLICATION_CREDENTIALS is set for authentication
    # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/your/credentials.json"
    
    sample_text = "Hello, this is a test of Google Cloud Text-to-Speech for plain text."
    audio_bytes = synthesize_text_to_audio(sample_text)
    
    with open("output_plain_text.mp3", "wb") as out:
        out.write(audio_bytes)
    print("Audio content written to file output_plain_text.mp3")
