from openai import OpenAI


def corpus_safety(texts):
    client = OpenAI()
    results = []
    for text in texts:
        moderation = client.moderations.create(model="omni-moderation-latest", input=text)
        results.append(moderation)
    return results
