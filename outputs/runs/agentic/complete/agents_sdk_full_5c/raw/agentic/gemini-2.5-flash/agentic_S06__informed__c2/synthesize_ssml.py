from google.cloud import texttospeech
import os

def synthesize_ssml(ssml_text: str, voice_name: str = "en-US-Wavenet-D", audio_encoding: texttospeech.AudioEncoding = texttospeech.AudioEncoding.MP3) -> bytes:
    """Synthesizes SSML with voice and prosody controls using Google Cloud Text-to-Speech.

    Args:
        ssml_text: The SSML text to synthesize.
        voice_name: The desired voice name (e.g., "en-US-Wavenet-D").
        audio_encoding: The desired audio encoding (e.g., MP3, LINEAR16).

    Returns:
        The audio content as bytes.
    """
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(ssml=ssml_text)
    voice = texttospeech.VoiceSelectionParams(
        language_code=voice_name.split('-')[0] + '-' + voice_name.split('-')[1],
        name=voice_name
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=audio_encoding
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    return response.audio_content

if __name__ == '__main__':
    # Example usage with SSML
    ssml = """<speak>Hello. <prosody rate="slow">This is some slower speech.</prosody> <emphasis>And this is emphasized.</emphasis></speak>"""
    audio_bytes = synthesize_ssml(ssml)
    
    print(f"Synthesized SSML audio size: {len(audio_bytes)} bytes")
