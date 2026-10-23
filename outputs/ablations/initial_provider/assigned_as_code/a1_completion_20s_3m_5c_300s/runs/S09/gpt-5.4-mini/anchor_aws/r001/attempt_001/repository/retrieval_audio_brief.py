import os

from openai import OpenAI


def retrieval_audio_brief(payload, config=None):
    config = config or {}
    client = OpenAI(api_key=config.get("api_key", os.getenv("OPENAI_API_KEY")))
    context = "\n".join(payload["results"])
    response = client.responses.create(
        model=config.get("model", "gpt-4o-mini-tts"),
        input=[
            {"role": "system", "content": "Write a short spoken brief from the retrieved results."},
            {"role": "user", "content": context},
        ],
    )
    return {"brief": response.output_text}
