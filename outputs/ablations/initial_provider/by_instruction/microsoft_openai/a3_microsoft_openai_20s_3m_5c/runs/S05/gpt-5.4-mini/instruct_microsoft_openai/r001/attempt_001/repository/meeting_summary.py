from openai import OpenAI

from speech_client import create_openai_client, load_speech_config


def summarize_meeting(transcript: str) -> str:
    config = load_speech_config()
    client: OpenAI = create_openai_client(config)
    response = client.responses.create(model="gpt-4o-mini", input=f"Summarize meeting transcript:\n{transcript}")
    return getattr(response, "output_text", "")
