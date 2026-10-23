from google.cloud import texttospeech
import os

def generate_audio_preview(payload, config=None):
    config = config or {}
    client = texttospeech.TextToSpeechClient()

    translated_copy = payload['translated_text']
    target_language_code = payload['target_language_code']
    voice_name = payload.get('voice_name', None) # Optional, can be specific like 'en-US-Wavenet-A'
    audio_encoding = payload.get('audio_encoding', texttospeech.AudioEncoding.MP3) # Default to MP3
    speaking_rate = payload.get('speaking_rate', 1.0) # Default speaking rate
    pitch = payload.get('pitch', 0.0) # Default pitch

    synthesis_input = texttospeech.SynthesisInput(text=translated_copy)

    # Select the language and SSML voice type
    if voice_name:
        voice = texttospeech.VoiceSelectionParams(
            language_code=target_language_code,
            name=voice_name
        )
    else:
        # Let Google Cloud Text-to-Speech choose a default voice for the language
        voice = texttospeech.VoiceSelectionParams(
            language_code=target_language_code,
            ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL # Or FEMALE/MALE/UNSPECIFIED
        )

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=audio_encoding,
        speaking_rate=speaking_rate,
        pitch=pitch
    )

    # Perform the text-to-speech request on the text input with the selected voice parameters and audio file type
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # The response's audio_content is binary. It can be saved directly as an audio file.
    # For this function, we'll return it as base64 encoded string or raw bytes if preferred.
    # For simplicity, returning raw bytes here. User can then save it to a file.
    
    # Note: In a real application, you might save this to a file or stream it.
    # Here we are returning the raw audio content directly.
    return {
        'translated_text': translated_copy,
        'audio_content': response.audio_content.hex(), # Returning as hex string for JSON compatibility
        'audio_encoding': audio_encoding.name,
        'target_language_code': target_language_code
    }
