import os
import google.cloud.texttospeech as tts

# Load credentials from environment variable (assumes GOOGLE_APPLICATION_CREDENTIALS is set)
client = tts.TextToSpeechClient()

def synthesize(text, voice_name=None, audio_encoding='LINEAR16'):
    """Synthesize plain text to an audio byte stream using Google Cloud Text-to-Speech.

    Args:
        text (str): Input text to synthesize.
        voice_name (str, optional): Specific voice name, e.g., "en-US-Wavenet-D".
        audio_encoding (str): Output encoding.

    Returns:
        bytes: Binary audio data.
    """
    voice = None
    if voice_name:
        voice = tts.VoiceSelectionParams(name=voice_name)
    input_data = tts.SynthesisInput(text=text)
    config = tts.VoiceSelectionParams(language_code='en-US')
    if voice:
        config.voice = voice
    config.audio_encoding = getattr(tts.AudioEncoding, audio_encoding)
    response = client.synthesize_speech(input=input_data, voice=config, audio_config=config)
    return response.audio_content

if __name__ == '__main__':
    sample = "Hello, world!"
    audio = synthesize(sample)
    print('Audio synthesized.')
