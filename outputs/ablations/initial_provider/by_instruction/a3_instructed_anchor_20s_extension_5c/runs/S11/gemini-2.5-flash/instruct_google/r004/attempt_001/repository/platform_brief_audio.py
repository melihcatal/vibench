from google.cloud import texttospeech

def platform_brief_audio(text_content: str, output_file_path: str = "output.mp3"):
    """Generates spoken briefings from Google Vertex AI platform outputs using Google Cloud Text-to-Speech API."""
    client = texttospeech.TextToSpeechClient()
    
    synthesis_input = texttospeech.SynthesisInput(text=text_content)
    
    # Select the language and SSML Voice type
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )
    
    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )
    
    # Perform the text-to-speech request
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )
    
    # The response's audio_content is binary. Write it to an output file.
    with open(output_file_path, "wb") as out:
        out.write(response.audio_content)
        
    return {"text": text_content, "audio_file": output_file_path}
