from model_client import get_model_client
import base64

def generate_audio_brief(text: str, output_file: str) -> None:
    client = get_model_client()
    response = client.audio.speech.create(
        model="tts-1",  # Concrete OpenAI TTS model identifier
        voice="alloy",
        input=text
    )
    response.stream_to_file(output_file)