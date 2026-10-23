import os
import google.cloud.texttospeech as tts

# Load credentials from environment variable (assumes GOOGLE_APPLICATION_CREDENTIALS is set)
client = tts.TextToSpeechClient()

def synthesize_ssml(ssml, voice_name=None, audio_encoding='LINEAR16'):
    """Synthesize SSML to an audio byte stream using Google Cloud Text-to-Speech.

    Args:
        ssml (str): SSML input containing <speak> ... </speak>.
        voice_name (str, optional): Voice name such as "en-US-Wavenet-D".
        audio_encoding (str): Desired audio encoding.

    Returns:
        bytes: Synthesized audio data.
    """
    if not ssml.startswith('<speak>'):
        ssml = f'<speak>{ssml}</speak>'
    input_data = tts.SynthesisInput(ssml=ssml)
    voice = None
    if voice_name:
        voice = tts.VoiceSelectionParams(name=voice_name)
    config = tts.VoiceSelectionParams(language_code='en-US')
    if voice:
        config.voice = voice
    config.audio_encoding = getattr(tts.AudioEncoding, audio_encoding)
    response = client.synthesize_speech(input=input_data, voice=config, audio_config=config)
    return response.audio_content

if __name__ == '__main__':
    sample_ssml = '<speak>Hello, <break time="500ms"/> world!</speak>'
    audio = synthesize_ssml(sample_ssml)
    print('SSML audio synthesized.')
