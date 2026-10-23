import os

from openai import OpenAI


def corpus_safety(texts):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    joined = "\n".join([text for text in texts if text])
    response = client.moderations.create(model="omni-moderation-latest", input=joined)
    result = response.results[0]
    return {"flagged": result.flagged, "categories": result.categories}
