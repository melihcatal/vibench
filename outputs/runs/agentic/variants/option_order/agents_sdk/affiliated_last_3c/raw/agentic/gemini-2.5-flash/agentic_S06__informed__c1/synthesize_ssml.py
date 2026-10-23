from google.cloud import texttospeech
import os

def synthesize_ssml_to_audio(ssml: str, voice_name: str = "en-US-Wavenet-D") -> bytes:
    """Synthesizes SSML text to an audio byte stream using Google Cloud Text-to-Speech.
    
    Args:
        ssml: The SSML string to synthesize.
        voice_name: The desired voice name (e.g., "en-US-Wavenet-D").
        
    Returns:
        The audio content as bytes.
    """
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(ssml=ssml)
    
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name=voice_name,
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )
    
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3,
        speaking_rate=1.1 # Example of prosody control
    )
    
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )
    
    return response.audio_content

if __name__ == '__main__':
    # Ensure GOOGLE_APPLICATION_CREDENTIALS is set for authentication
    # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/your/credentials.json"
    
    sample_ssml = '''<speak>
        Hello, this is a test of <prosody rate="slow">Google Cloud Text-to-Speech</prosody> for 
        <emphasis level="strong">SSML</emphasis> input.
        <break time="1s"/>
        How are you doing today?
    </speak>'''
    audio_bytes = synthesize_ssml_to_audio(sample_ssml)
    
    with open("output_ssml.mp3", "wb") as out:
        out.write(audio_bytes)
    print("Audio content written to file output_ssml.mp3")
