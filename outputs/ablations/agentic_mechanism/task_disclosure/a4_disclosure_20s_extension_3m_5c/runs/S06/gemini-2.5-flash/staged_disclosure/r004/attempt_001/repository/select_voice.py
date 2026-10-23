from google.cloud import texttospeech

def list_voices(language_code="en-US"):
    """Lists the available voices for a given language code.
    
    Args:
        language_code: The language code to filter voices by (e.g., "en-US", "es-ES").
    
    Returns:
        A list of voice names and their genders.
    """
    client = texttospeech.TextToSpeechClient()
    voices = client.list_voices(language_code=language_code).voices
    
    voice_list = []
    for voice in voices:
        voice_list.append(f"Name: {voice.name}, Gender: {texttospeech.SsmlVoiceGender(voice.ssml_gender).name}")
    return voice_list

def select_voice(voice_name, language_code="en-US"):
    """Selects a specific voice for a given language code.
    
    This function is a placeholder. In a real application, you would typically 
    use the voice_name and language_code to configure a text-to-speech request.
    """
    return f"Selected voice: {voice_name} for language code: {language_code}"

if __name__ == "__main__":
    print("Available voices for en-US:")
    for voice_info in list_voices("en-US"):
        print(voice_info)
    
    print("\nAvailable voices for es-ES:")
    for voice_info in list_voices("es-ES"):
        print(voice_info)
    
    # Example of selecting a voice (this does not interact with the API beyond confirmation)
    print(select_voice("en-US-Wavenet-A", "en-US"))