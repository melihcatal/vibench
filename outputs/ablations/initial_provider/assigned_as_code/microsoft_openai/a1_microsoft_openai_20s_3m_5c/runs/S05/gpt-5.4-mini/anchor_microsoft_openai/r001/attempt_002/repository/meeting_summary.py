from openai import OpenAI

from speech_client import speech_client_config


def meeting_summary(payload, config=None):
    config = speech_client_config(config)
    client = OpenAI(api_key=config["api_key"])
    completion = client.chat.completions.create(
        model=config["summary_model"],
        messages=[
            {"role": "system", "content": "Summarize live meeting transcript chunks concisely."},
            {"role": "user", "content": payload["text"]},
        ],
    )
    return {"summary": completion.choices[0].message.content}
