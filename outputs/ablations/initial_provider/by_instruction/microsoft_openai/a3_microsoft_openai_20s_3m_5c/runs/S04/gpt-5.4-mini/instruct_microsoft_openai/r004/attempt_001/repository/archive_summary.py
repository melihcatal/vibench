from openai import OpenAI

from speech_client import load_config


def archive_summary(transcript: str):
    config = load_config("openai")
    client = OpenAI(api_key=config.api_key)
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {"role": "system", "content": "Summarize the transcript for archival storage."},
            {"role": "user", "content": transcript},
        ],
    )
    return response.output_text
