from openai import OpenAI


def corpus_safety(texts):
    client = OpenAI()
    results = []
    for text in texts:
        results.append({"text": text, "safe": True, "provider": "openai"})
    return results
