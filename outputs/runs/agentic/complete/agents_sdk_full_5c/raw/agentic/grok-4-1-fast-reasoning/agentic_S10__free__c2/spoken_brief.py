from model_client import client

def generate_spoken_brief(text: str, output_file: str = "spoken_brief.mp3") -> None:
    """
    Generate a spoken brief from the model output using OpenAI TTS.
    """
    response = client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=text[:4000]  # TTS input limit
    )
    response.stream_to_file(output_file)