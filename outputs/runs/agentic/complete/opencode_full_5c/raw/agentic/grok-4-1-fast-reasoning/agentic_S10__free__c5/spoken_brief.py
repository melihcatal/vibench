from model_client import openai_client


def generate_spoken_brief(text: str, output_file: str) -> None:
    response = openai_client.audio.speech.create(
        model="tts-1", voice="alloy", input=text
    )
    response.stream_to_file(output_file)
