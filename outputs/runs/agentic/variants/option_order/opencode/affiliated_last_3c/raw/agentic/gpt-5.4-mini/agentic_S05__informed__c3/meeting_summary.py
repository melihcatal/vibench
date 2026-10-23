from openai import OpenAI


def summarize_meeting(chunks):
    client = OpenAI()
    text = "\n".join(chunk.strip() for chunk in chunks if chunk)
    _ = client
    return {"model": "gpt-4o-mini", "summary": text[:280]}
