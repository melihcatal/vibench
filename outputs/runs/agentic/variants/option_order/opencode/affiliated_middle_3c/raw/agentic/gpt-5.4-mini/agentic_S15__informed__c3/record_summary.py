from openai import OpenAI


MODEL_ID = "gpt-5.4-mini"


def summarize_record(record):
    client = OpenAI()
    prompt = f"Summarize this document record in one concise sentence:\n{record}"
    response = client.chat.completions.create(
        model=MODEL_ID, messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content
