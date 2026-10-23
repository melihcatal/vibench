import os

from openai import OpenAI


def multilingual_query_translate(payload, config=None):
    config = config or {}
    client = OpenAI(api_key=config.get("api_key", os.getenv("OPENAI_API_KEY")))
    response = client.chat.completions.create(
        model=config.get("model", "gpt-4o-mini"),
        messages=[
            {"role": "system", "content": "Translate the query into English for embedding search."},
            {"role": "user", "content": payload["query"]},
        ],
        temperature=0,
    )
    return {"translated_query": response.choices[0].message.content}
