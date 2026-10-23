from google.cloud import texttospeech
from speech_client import get_text_to_speech_client
from speech_models import SynthesisRequest

def synthesize_ssml(request: SynthesisRequest) -> bytes:
    client = get_text_to_speech_client()
    synthesis_input = texttospeech.SynthesisInput(ssml=request.ssml)
    voice = texttospeech.VoiceSelectionParams(
        language_code=request.language_code,
        name=request.voice_name
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )
    return response.audio_content

if __name__ == '__main__':
    # Example usage (requires credentials)
    ssml_text = "'''<speak>Hello, <prosody rate="slow">world!</prosody> This is a <emphasis level="strong">SSML</emphasis> test.</speak>'''"
    req = SynthesisRequest(ssml=ssml_text, language_code="en-US", voice_name="en-US-Standard-A")
    audio_bytes = synthesize_ssml(req)
    print(f"Synthesized {len(audio_bytes)} bytes of audio from SSML.")
