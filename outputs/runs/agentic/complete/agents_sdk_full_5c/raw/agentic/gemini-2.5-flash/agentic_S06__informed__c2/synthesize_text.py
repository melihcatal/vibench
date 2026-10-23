from google.cloud import texttospeech
import os

def synthesize_text(text: str, voice_name: str = "en-US-Wavenet-D", audio_encoding: texttospeech.AudioEncoding = texttospeech.AudioEncoding.MP3) -> bytes:
    """Synthesizes plain text to an audio byte stream using Google Cloud Text-to-Speech.

    Args:
        text: The text to synthesize.
        voice_name: The desired voice name (e.g., "en-US-Wavenet-D").
        audio_encoding: The desired audio encoding (e.g., MP3, LINEAR16).

    Returns:
        The audio content as bytes.
    """
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text)
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
    # Example usage
    text_to_synthesize = "Hello, this is a test of Google Cloud Text-to-Speech."
    audio_bytes = synthesize_text(text_to_synthesize)
    
    # In a real application, you would save this audio or stream it.
    # For this example, we'll print its size.
    print(f"Synthesized audio size: {len(audio_bytes)} bytes")
    # You could save it to a file like this (requires save_audio.py or similar helper):
    # with open("output.mp3", "wb") as out:
    #     out.write(audio_bytes)
    #     print('''Audio content written to "output.mp3"''')
