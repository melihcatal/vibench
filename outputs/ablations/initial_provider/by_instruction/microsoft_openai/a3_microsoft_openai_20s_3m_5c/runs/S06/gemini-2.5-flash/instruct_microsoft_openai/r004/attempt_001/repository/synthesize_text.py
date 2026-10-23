from speech_client import OpenAIClient
from speech_models import SynthesisInput, SynthesisOutput

def synthesize_text(input: SynthesisInput) -> SynthesisOutput:
    client = OpenAIClient()
    response = client.audio.speech.create(
        model="tts-1",  # OpenAI TTS model
        voice=input.voice_id,
        input=input.text,
    )
    audio_content = response.content
    return SynthesisOutput(audio_content=audio_content, audio_format="mp3")
