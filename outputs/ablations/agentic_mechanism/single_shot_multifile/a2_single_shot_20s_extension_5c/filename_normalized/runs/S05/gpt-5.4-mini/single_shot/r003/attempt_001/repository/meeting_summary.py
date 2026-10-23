from openai import OpenAI

from speech_client import load_speech_config


def summarize_meeting_transcript(chunks: list[str]) -> str:
    config = load_speech_config()
    client = OpenAI(api_key=config.api_key or None)
    transcript = "\n".join(chunks)
    response = client.responses.create(
        model="gpt-4o-mini",
        input=[
            {
                "role": "system",
                "content": "Summarize the meeting transcript into concise action-oriented notes.",
            },
            {
                "role": "user",
                "content": transcript,
            },
        ],
    )
    return response.output_text
